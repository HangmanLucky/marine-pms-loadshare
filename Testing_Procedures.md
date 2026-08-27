# Functional Test Procedure — PMS Power Management

**Project:** Autonomous Marine Power Management System (PMS)
**Document type:** Factory Acceptance Test (FAT) — simulated / desktop validation
**Author:** Sipho Lucky Sibanda

| # | Test Case | Precondition | Action | Expected Result | Pass/Fail |
|---|------------|----------------|---------|--------------------|-------------|
| 1 | Normal single-generator operation | Gen1 running, breaker closed, light load | Observe steady state | Status "NORMAL - GEN1 DUTY"; no shed stages active | |
| 2 | Fast load shed on unexpected Gen1 trip | Gen1 carrying &gt;90% of single-gen capacity | Force `DI_Gen1_Breaker_Closed = FALSE` without blackout conditions | Stage 1 (and 2/3 as needed) shed within one scan; `Alarm_Overload` raised | |
| 3 | Load-dependent auto-start | Gen1 load rises above 85% rated | Ramp `AI_Gen1_Load_kW` upward | `PMS_State` moves to STARTING; `DO_Gen2_Start` energises | |
| 4 | Full auto-sync sequence | Gen2 started, bus live | Let sequence run: warm-up &rarr; speed match &rarr; voltage match &rarr; phase match &rarr; close | `PMS_State` reaches RUNNING_PARALLEL; `DI_Gen2_Breaker_Closed` confirmed | |
| 5 | Sync timeout — frequency never matches | In SPEED_MATCH | Hold `AI_Gen2_Freq_Hz` far from `AI_BusFreq_Hz` past `T_SyncWindow_PT` | `PMS_State` &rarr; SYNC_FAILED; `Alarm_SyncTimeout` raised; breaker never commanded closed | |
| 6 | Sync retry requires fresh request | Continuing from Test 5 | Drop `DI_ManualSyncRequest`, then re-raise it | State returns to IDLE, then a fresh sync attempt can start — no silent auto-retry | |
| 7 | Breaker close confirmation failure | In CLOSE_BREAKER, all sync conditions met | Withhold `DI_Gen2_Breaker_Closed` feedback past `T_BreakerConfirm_PT` | `PMS_State` &rarr; SYNC_FAILED; close command drops | |
| 8 | Full blackout detection | Both generators tripped, bus dead | Force both `DI_GenX_Running = FALSE`, `AI_BusVoltage_V` below threshold | `BlackoutDetected` TRUE; `PMS_State` &rarr; BLACKOUT_EMERGENCY within one scan | |
| 9 | Emergency generator auto-start | Continuing from Test 8 | Observe | `DO_EmergencyGen_Start` energises; all three load-shed stages force TRUE | |
| 10 | Black-start dead-bus close | Emergency gen running, Gen1 restarted | Confirm `DI_Gen1_Running`, warm-up elapsed, bus still dead | `DO_Gen1_Breaker_Close` issued directly — **no** synchronising states entered | |
| 11 | Staged load restoration | Gen1 breaker closed after blackout | Observe over time | Stage 3 clears first, then Stage 2, then Stage 1, each gated by `T_RestoreStage_PT`; no simultaneous restoration | |
| 12 | Blackout recovery completes to normal | Continuing from Test 11 | Wait for all stages to clear | `PMS_State` &rarr; IDLE; `Alarm_Blackout` clears; normal load-dependent logic resumes | |

## Why Tests 5–7 matter as much as the "happy path"

Test 4 (a clean sync) is necessary but not sufficient. A synchroniser that can't
fail safely — that might close a breaker out of phase because a timeout wasn't
enforced, or that retries endlessly against a genset with a real fault — is a worse
outcome than no automation at all. Tests 5–7 specifically prove the sequence aborts
cleanly and never issues a breaker-close command unless every condition was verified
in that same cycle.

## How to exercise these tests without physical hardware

As with the other two projects, these cases were run by forcing input tags in a
PLCSIM-style watch table (or an equivalent CODESYS soft-PLC harness). Tests 8–12
specifically were run as one continuous scripted sequence to confirm the blackout
recovery state chain behaves correctly end-to-end, not just at each isolated state.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Test performed by | Sipho Lucky Sibanda | |
| Reviewed by | | |
