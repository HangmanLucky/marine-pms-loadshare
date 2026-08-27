# I/O List — Marine Power Management System (PMS)

**Project:** Intelligent Load-Shedding &amp; Blackout Recovery
**Author:** Sipho Lucky Sibanda
**Target platform:** Siemens S7-1500 (TIA Portal / SCL) — portable to a CODESYS-based
marine PMS controller

## Inputs

| Tag Name                 | Description                                     | Signal Type      | Range / Units       |
|-----------------------------|----------------------------------------------------|--------------------|-------------------------|
| `AI_Gen1_Load_kW`            | Gen1 active power (from power meter/CT)             | 4–20 mA             | 0–2200 kW                |
| `AI_Gen2_Load_kW`            | Gen2 active power                                    | 4–20 mA             | 0–2200 kW                |
| `AI_Gen2_Freq_Hz`             | Gen2 (incoming set) frequency                        | Sync relay / AI      | 45–65 Hz                  |
| `AI_BusFreq_Hz`                | Main busbar frequency                                | Frequency relay      | 45–65 Hz                  |
| `AI_Gen2_Voltage_V`            | Gen2 terminal voltage                                | Sync relay / AI      | 0–500 V                    |
| `AI_BusVoltage_V`                | Main busbar voltage                                  | PT / voltage relay    | 0–500 V                    |
| `AI_PhaseAngle_Deg`               | Synchronising relay output, Gen2 vs Bus               | Sync relay / AI        | -180 – +180&deg;             |
| `DI_Gen1_Running`                   | Gen1 engine running feedback                          | Digital (24VDC)          | 0/1                            |
| `DI_Gen2_Running`                     | Gen2 engine running feedback                          | Digital (24VDC)            | 0/1                              |
| `DI_Gen1_Breaker_Closed`                | Gen1 breaker auxiliary contact                        | Digital (24VDC)              | 0/1                                |
| `DI_Gen2_Breaker_Closed`                  | Gen2 breaker auxiliary contact                        | Digital (24VDC)                | 0/1                                  |
| `DI_EmergencyGen_Running`                   | Emergency generator running feedback                  | Digital (24VDC)                  | 0/1                                    |
| `DI_ManualSyncRequest`                        | Operator pushbutton, request Gen2 parallel             | Digital (24VDC)                    | 0/1                                      |
| `DI_System_Enable`                               | Master enable                                          | Digital (24VDC)                      | 0/1                                        |

## Outputs

| Tag Name                     | Description                                       | Signal Type          |
|---------------------------------|--------------------------------------------------------|--------------------------|
| `DO_Gen1_Start`                    | Black-start command to Gen1                              | Digital (24VDC)            |
| `DO_Gen2_Start`                      | Start command to Gen2                                     | Digital (24VDC)              |
| `DO_Gen1_Breaker_Close`                | Gen1 dead-bus reclose command (blackout recovery only)     | Digital (24VDC)                |
| `DO_Gen2_Breaker_Close`                  | Gen2 breaker close command (pulsed, live sync only)          | Digital (24VDC)                  |
| `AO_Gen2_GovernorBias_Pct`                 | Speed trim to Gen2 governor during synchronising               | 4–20 mA, -100&ndash;100%           |
| `AO_Gen2_AVRBias_Pct`                        | Voltage trim to Gen2 AVR during synchronising                    | 4–20 mA, -100&ndash;100%             |
| `DO_LoadShed_Stage1`                           | Trips galley / laundry load group                                  | Digital (24VDC)                        |
| `DO_LoadShed_Stage2`                             | Trips accommodation HVAC load group                                  | Digital (24VDC)                          |
| `DO_LoadShed_Stage3`                               | Trips non-essential deck machinery load group                          | Digital (24VDC)                            |
| `DO_EmergencyGen_Start`                              | Start command to the emergency generator                                | Digital (24VDC)                              |
| `Alarm_Overload`                                        | Load shedding active / overload risk                                     | Digital (24VDC)                                |
| `Alarm_Blackout`                                          | Blackout recovery in progress                                              | Digital (24VDC)                                  |
| `Alarm_SyncTimeout`                                          | Auto-sync sequence failed to complete in time                                | Digital (24VDC)                                    |
| `PMS_State`                                                     | Current state machine state (enumeration, for HMI/diagnostics)                | Internal / HMI tag                                   |
| `SystemStatus`                                                     | Human-readable status text                                                     | STRING, HMI tag                                        |

## Notes for reviewers

- **Steering gear, navigation equipment, and fire pumps are not wired to any
  `DO_LoadShed_*` output.** They're protected by omission rather than by a software
  interlock — the sheddable load groups only ever include galley, laundry,
  accommodation HVAC, and non-essential deck machinery. This mirrors how vital-load
  segregation is actually done on a real switchboard (separate, unsheddable
  distribution sections).
- `Gen_Rated_kW`, load-shed block sizes, and all tolerances are declared as internal
  `VAR` constants in `PMS_PowerManagement.st`. On a real vessel these would be
  commissioned per the actual generator nameplate rating and the ship's specific
  load schedule, not left at the illustrative defaults shown here.
- The emergency generator itself (its own start batteries/air, fuel supply, and
  switchboard) is treated as a self-contained unit per SOLAS — this function block
  only issues the start command and watches its running feedback, it does not model
  the emergency generator's own internal control.
