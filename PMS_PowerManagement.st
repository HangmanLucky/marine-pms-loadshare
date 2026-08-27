(*
====================================================================================
  PROJECT   : Autonomous Marine Power Management System (PMS)
              Intelligent Load-Shedding & Blackout Recovery
  MODULE    : FB_PMS_PowerManagement
  PLATFORM  : IEC 61131-3 Structured Text
              Written against Siemens SCL (TIA Portal, S7-1500) syntax,
              portable to CODESYS-based marine PMS controllers.
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : A vessel's electrical plant normally runs one duty generator
              (Gen1) carrying the ship's load. Gen2 is a standby/duty-
              standby set. This function block covers three linked
              responsibilities of a marine PMS:
                1. FAST LOAD SHEDDING   - if Gen1 trips unexpectedly, shed
                   non-essential load in well under a second so whatever
                   remains never sees an overload it can't carry.
                2. AUTO-SYNCHRONISING   - bring Gen2 online and close its
                   breaker onto a LIVE busbar without tripping the plant,
                   whether requested by the operator or by rising load.
                3. BLACKOUT RECOVERY    - if the plant blacks out entirely,
                   start the emergency generator, black-start the main
                   plant onto the (now confirmed) dead bus, and restore
                   load in controlled stages.

  REGULATORY / STANDARDS BASIS (simulated against, for realism only):
    - SOLAS Chapter II-1, Reg. 42/43   : Emergency source of electrical
                                          power (45-second start requirement)
                                          and its distribution.
    - IEC 61892-1 / IEC 60092 series   : Electrical installations on ships
                                          and offshore units.
    - Class society PMS guidance       : e.g. DNV-RU-SHIP Pt.4 Ch.8 on
                                          power management systems.
====================================================================================
*)

TYPE E_PMS_State :
(
    ST_IDLE,
    ST_STARTING,
    ST_WARMUP,
    ST_SPEED_MATCH,
    ST_VOLTAGE_MATCH,
    ST_PHASE_MATCH,
    ST_CLOSE_BREAKER,
    ST_RUNNING_PARALLEL,
    ST_SYNC_FAILED,
    ST_BLACKOUT_EMERGENCY,
    ST_BLACKOUT_BLACKSTART,
    ST_BLACKOUT_RESTORE
);
END_TYPE

FUNCTION_BLOCK FB_PMS_PowerManagement
VAR_INPUT
    AI_Gen1_Load_kW          : REAL;   // Gen1 active power
    AI_Gen2_Load_kW          : REAL;   // Gen2 active power
    AI_Gen2_Freq_Hz           : REAL;   // Gen2 (incoming set) frequency
    AI_BusFreq_Hz              : REAL;   // Main busbar frequency
    AI_Gen2_Voltage_V         : REAL;   // Gen2 terminal voltage
    AI_BusVoltage_V             : REAL;   // Main busbar voltage
    AI_PhaseAngle_Deg           : REAL;   // Synchronising relay: Gen2 vs Bus, degrees
    DI_Gen1_Running             : BOOL;
    DI_Gen2_Running             : BOOL;
    DI_Gen1_Breaker_Closed      : BOOL;
    DI_Gen2_Breaker_Closed      : BOOL;
    DI_EmergencyGen_Running     : BOOL;
    DI_ManualSyncRequest        : BOOL;   // Operator request to parallel Gen2
    DI_System_Enable            : BOOL;
END_VAR

VAR_OUTPUT
    DO_Gen1_Start                : BOOL := FALSE;  // Black-start command
    DO_Gen2_Start                 : BOOL := FALSE;
    DO_Gen1_Breaker_Close          : BOOL := FALSE; // Dead-bus reclose after blackout
    DO_Gen2_Breaker_Close           : BOOL := FALSE; // Pulsed close command (live sync)
    AO_Gen2_GovernorBias_Pct         : REAL := 0.0;  // Speed trim, -100..100%
    AO_Gen2_AVRBias_Pct               : REAL := 0.0;  // Voltage trim, -100..100%
    DO_LoadShed_Stage1                 : BOOL := FALSE; // Galley / laundry
    DO_LoadShed_Stage2                  : BOOL := FALSE; // Accommodation HVAC
    DO_LoadShed_Stage3                   : BOOL := FALSE; // Non-essential deck machinery
    DO_EmergencyGen_Start                 : BOOL := FALSE;
    Alarm_Overload                         : BOOL := FALSE;
    Alarm_Blackout                          : BOOL := FALSE;
    Alarm_SyncTimeout                        : BOOL := FALSE;
    PMS_State                                 : E_PMS_State := ST_IDLE;
    SystemStatus                               : STRING[24] := 'STANDBY';
END_VAR

VAR
    // --- Ratings & thresholds ---
    Gen_Rated_kW            : REAL := 2000.0;
    LoadShed_Stage1_kW      : REAL := 150.0;   // Estimated block shed at stage 1
    LoadShed_Stage2_kW      : REAL := 300.0;
    LoadShed_Stage3_kW      : REAL := 200.0;
    Overload_Margin_Pct     : REAL := 90.0;    // Shed before hitting 100% capacity
    Freq_Tolerance_Hz       : REAL := 0.10;
    Volt_Tolerance_Pct      : REAL := 2.0;
    PhaseClose_Window_Deg   : REAL := 8.0;     // Close within this angle, leading zero
    DeadBus_Threshold_V     : REAL := 50.0;    // Below this, bus is considered dead

    // --- Derived / working values ---
    RunningGenCount          : INT;
    TotalLoad_kW             : REAL;
    AvailableCapacity_kW     : REAL;
    BusIsDead                : BOOL;
    BlackoutDetected          : BOOL;
    TempBias                  : REAL;
    VoltErrPct                 : REAL;

    // --- Edge detection for fast load shed ---
    Gen1_Was_Running           : BOOL;
    Gen1_TripEdge               : BOOL;

    // --- State machine timers ---
    T_Start                      : TON;  T_Start_PT    : TIME := T#20S;
    T_Warmup                      : TON;  T_Warmup_PT   : TIME := T#30S;
    T_SyncWindow                   : TON;  T_SyncWindow_PT : TIME := T#60S;
    T_BreakerConfirm                 : TON;  T_BreakerConfirm_PT : TIME := T#500MS;
    T_RestoreStage                     : TON;  T_RestoreStage_PT : TIME := T#15S;

    RestoreStageIndex                   : INT := 0;
END_VAR

// ------------------------------------------------------------------
// 1. BUS & GENERATOR STATUS
// ------------------------------------------------------------------
RunningGenCount := 0;
IF DI_Gen1_Running AND DI_Gen1_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF
IF DI_Gen2_Running AND DI_Gen2_Breaker_Closed THEN RunningGenCount := RunningGenCount + 1; END_IF

TotalLoad_kW := 0.0;
IF DI_Gen1_Breaker_Closed THEN TotalLoad_kW := TotalLoad_kW + AI_Gen1_Load_kW; END_IF
IF DI_Gen2_Breaker_Closed THEN TotalLoad_kW := TotalLoad_kW + AI_Gen2_Load_kW; END_IF

AvailableCapacity_kW := INT_TO_REAL(RunningGenCount) * Gen_Rated_kW;
BusIsDead              := AI_BusVoltage_V < DeadBus_Threshold_V;
BlackoutDetected        := DI_System_Enable AND BusIsDead
                            AND (NOT DI_Gen1_Running) AND (NOT DI_Gen2_Running);

// ------------------------------------------------------------------
// 2. FAST LOAD SHEDDING
//    Detects Gen1 dropping off the bus WITHOUT a full blackout, and
//    sheds pre-defined load blocks immediately - no iterative
//    calculation, because there is no time for one.
// ------------------------------------------------------------------
Gen1_TripEdge     := Gen1_Was_Running AND (NOT DI_Gen1_Breaker_Closed) AND (NOT BlackoutDetected);
Gen1_Was_Running  := DI_Gen1_Breaker_Closed;

IF (PMS_State <> ST_BLACKOUT_EMERGENCY) AND (PMS_State <> ST_BLACKOUT_BLACKSTART)
   AND (PMS_State <> ST_BLACKOUT_RESTORE) THEN
    IF Gen1_TripEdge OR (TotalLoad_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0)) THEN
        DO_LoadShed_Stage1 := TRUE;
        IF TotalLoad_kW - LoadShed_Stage1_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
            DO_LoadShed_Stage2 := TRUE;
        END_IF
        IF TotalLoad_kW - LoadShed_Stage1_kW - LoadShed_Stage2_kW > AvailableCapacity_kW * (Overload_Margin_Pct / 100.0) THEN
            DO_LoadShed_Stage3 := TRUE;
        END_IF
        Alarm_Overload := TRUE;
    ELSIF TotalLoad_kW < AvailableCapacity_kW * 0.6 THEN
        // Restore only once load has genuine margin back - avoids shed/restore chatter
        DO_LoadShed_Stage1 := FALSE;
        DO_LoadShed_Stage2 := FALSE;
        DO_LoadShed_Stage3 := FALSE;
        Alarm_Overload      := FALSE;
    END_IF
END_IF

// ------------------------------------------------------------------
// 3. BLACKOUT PRE-EMPTS EVERYTHING ELSE
// ------------------------------------------------------------------
IF BlackoutDetected AND (PMS_State <> ST_BLACKOUT_EMERGENCY)
   AND (PMS_State <> ST_BLACKOUT_BLACKSTART) AND (PMS_State <> ST_BLACKOUT_RESTORE) THEN
    PMS_State           := ST_BLACKOUT_EMERGENCY;
    DO_LoadShed_Stage1  := TRUE;   // Force everything non-essential OFF before
    DO_LoadShed_Stage2  := TRUE;   // power is restored, so nothing re-energises
    DO_LoadShed_Stage3  := TRUE;   // uncontrolled the instant the bus comes back.
    DO_Gen2_Start        := FALSE;
    RestoreStageIndex     := 0;
END_IF

// ------------------------------------------------------------------
// 4. LOAD-DEPENDENT AUTO-START TRIGGER
//    Proactively bring Gen2 online BEFORE an overload happens - distinct
//    from the reactive load-shed in section 2.
// ------------------------------------------------------------------
IF DI_System_Enable AND (NOT BlackoutDetected) AND (PMS_State = ST_IDLE)
   AND ((TotalLoad_kW > Gen_Rated_kW * 0.85) OR DI_ManualSyncRequest)
   AND (NOT DI_Gen2_Breaker_Closed) THEN
    PMS_State := ST_STARTING;
END_IF

// ------------------------------------------------------------------
// 5. AUTO-SYNCHRONISING STATE MACHINE (Gen2 onto a LIVE bus)
// ------------------------------------------------------------------
CASE PMS_State OF

    ST_STARTING:
        DO_Gen2_Start := TRUE;
        T_Start(IN := TRUE, PT := T_Start_PT);
        IF DI_Gen2_Running THEN
            T_Start(IN := FALSE);
            T_Warmup(IN := TRUE, PT := T_Warmup_PT);
            PMS_State := ST_WARMUP;
        ELSIF T_Start.Q THEN
            PMS_State := ST_SYNC_FAILED;
        END_IF

    ST_WARMUP:
        T_Warmup(IN := TRUE, PT := T_Warmup_PT);
        IF T_Warmup.Q THEN
            T_Warmup(IN := FALSE);
            T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
            PMS_State := ST_SPEED_MATCH;
        END_IF

    ST_SPEED_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        // Run the incoming set marginally fast so the phase angle steadily
        // advances toward the closing window, rather than drifting randomly.
        TempBias := (AI_BusFreq_Hz + 0.05 - AI_Gen2_Freq_Hz) * 50.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_GovernorBias_Pct := TempBias;

        IF ABS(AI_BusFreq_Hz - AI_Gen2_Freq_Hz) <= Freq_Tolerance_Hz THEN
            PMS_State := ST_VOLTAGE_MATCH;
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_VOLTAGE_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        VoltErrPct := ((AI_BusVoltage_V - AI_Gen2_Voltage_V) / AI_BusVoltage_V) * 100.0;
        TempBias    := VoltErrPct * 20.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_AVRBias_Pct := TempBias;

        IF ABS(VoltErrPct) <= Volt_Tolerance_Pct THEN
            PMS_State := ST_PHASE_MATCH;
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_PHASE_MATCH:
        T_SyncWindow(IN := TRUE, PT := T_SyncWindow_PT);
        // Keep trimming speed/voltage while waiting for the closing window -
        // synchronising is a moving target, not a one-shot check.
        TempBias := (AI_BusFreq_Hz + 0.05 - AI_Gen2_Freq_Hz) * 50.0;
        IF TempBias > 100.0 THEN TempBias := 100.0; END_IF
        IF TempBias < -100.0 THEN TempBias := -100.0; END_IF
        AO_Gen2_GovernorBias_Pct := TempBias;

        IF (AI_PhaseAngle_Deg <= 0.0) AND (AI_PhaseAngle_Deg > -PhaseClose_Window_Deg) THEN
            PMS_State := ST_CLOSE_BREAKER;
            T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
        END_IF
        IF T_SyncWindow.Q THEN PMS_State := ST_SYNC_FAILED; END_IF

    ST_CLOSE_BREAKER:
        DO_Gen2_Breaker_Close := TRUE;
        T_BreakerConfirm(IN := TRUE, PT := T_BreakerConfirm_PT);
        IF DI_Gen2_Breaker_Closed THEN
            DO_Gen2_Breaker_Close := FALSE;
            T_BreakerConfirm(IN := FALSE);
            T_SyncWindow(IN := FALSE);
            AO_Gen2_GovernorBias_Pct := 0.0;   // Hand over to load-sharing (droop)
            AO_Gen2_AVRBias_Pct       := 0.0;   // control - out of scope for this FB
            PMS_State := ST_RUNNING_PARALLEL;
        ELSIF T_BreakerConfirm.Q THEN
            DO_Gen2_Breaker_Close := FALSE;
            PMS_State := ST_SYNC_FAILED;
        END_IF

    ST_RUNNING_PARALLEL:
        // Stable end state. No automatic unload/stop sequence is modelled -
        // stopping Gen2 is left as an operator decision (see manual, Ch.10).
        IF NOT DI_Gen2_Breaker_Closed THEN
            PMS_State := ST_IDLE;
        END_IF

    ST_SYNC_FAILED:
        DO_Gen2_Start           := FALSE;
        Alarm_SyncTimeout        := TRUE;
        AO_Gen2_GovernorBias_Pct := 0.0;
        AO_Gen2_AVRBias_Pct       := 0.0;
        // Requires the operator to drop and re-raise the sync request before
        // another attempt - prevents a silent, unattended retry loop.
        IF NOT DI_ManualSyncRequest THEN
            Alarm_SyncTimeout := FALSE;
            PMS_State          := ST_IDLE;
        END_IF

    ST_BLACKOUT_EMERGENCY:
        DO_EmergencyGen_Start := TRUE;
        Alarm_Blackout          := TRUE;
        IF DI_EmergencyGen_Running THEN
            T_Warmup(IN := TRUE, PT := T_Warmup_PT);
            PMS_State := ST_BLACKOUT_BLACKSTART;
        END_IF

    ST_BLACKOUT_BLACKSTART:
        DO_Gen1_Start := TRUE;
        T_Warmup(IN := TRUE, PT := T_Warmup_PT);
        IF DI_Gen1_Running AND T_Warmup.Q AND BusIsDead THEN
            DO_Gen1_Breaker_Close := TRUE;   // Dead-bus close - no sync check needed,
        END_IF                                // the bus is confirmed dead, not live.
        IF DI_Gen1_Breaker_Closed THEN
            DO_Gen1_Breaker_Close := FALSE;
            T_Warmup(IN := FALSE);
            T_RestoreStage(IN := TRUE, PT := T_RestoreStage_PT);
            PMS_State := ST_BLACKOUT_RESTORE;
        END_IF

    ST_BLACKOUT_RESTORE:
        // Restore in the REVERSE order load was shed - last shed, first back -
        // each stage gated by a timer so the freshly-started plant is never
        // hit with the full return of load in one step.
        T_RestoreStage(IN := TRUE, PT := T_RestoreStage_PT);
        CASE RestoreStageIndex OF
            0:  IF T_RestoreStage.Q THEN
                    DO_LoadShed_Stage3 := FALSE;
                    T_RestoreStage(IN := FALSE);
                    RestoreStageIndex := 1;
                END_IF
            1:  IF T_RestoreStage.Q THEN
                    DO_LoadShed_Stage2 := FALSE;
                    T_RestoreStage(IN := FALSE);
                    RestoreStageIndex := 2;
                END_IF
            2:  IF T_RestoreStage.Q THEN
                    DO_LoadShed_Stage1 := FALSE;
                    T_RestoreStage(IN := FALSE);
                    RestoreStageIndex := 3;
                END_IF
            3:  Alarm_Blackout := FALSE;
                RestoreStageIndex := 0;
                PMS_State := ST_IDLE;
        END_CASE

    ELSE
        ; // ST_IDLE - nothing to do, section 4 above owns the transition out

END_CASE

// ------------------------------------------------------------------
// 6. STATUS TEXT
// ------------------------------------------------------------------
IF NOT DI_System_Enable THEN
    SystemStatus := 'STANDBY';
ELSIF BlackoutDetected OR (PMS_State = ST_BLACKOUT_EMERGENCY)
      OR (PMS_State = ST_BLACKOUT_BLACKSTART) OR (PMS_State = ST_BLACKOUT_RESTORE) THEN
    SystemStatus := 'BLACKOUT RECOVERY';
ELSIF PMS_State = ST_RUNNING_PARALLEL THEN
    SystemStatus := 'GENS PARALLEL';
ELSIF PMS_State = ST_SYNC_FAILED THEN
    SystemStatus := 'SYNC FAILED';
ELSIF (PMS_State <> ST_IDLE) THEN
    SystemStatus := 'SYNCHRONISING';
ELSIF Alarm_Overload THEN
    SystemStatus := 'LOAD SHED ACTIVE';
ELSE
    SystemStatus := 'NORMAL - GEN1 DUTY';
END_IF

END_FUNCTION_BLOCK
