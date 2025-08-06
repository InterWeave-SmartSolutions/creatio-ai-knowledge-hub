# Customize quartz task scheduler | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1999 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/classic-ui/task-scheduler

## Description

The functionality is relevant to Classic UI.

## Key Concepts

configuration, classic ui, synchronization, lead, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

note

The functionality is relevant to Classic UI.

## Recommendations on scheduler setup​

All Quartz policies for the processing of overdue tasks can be divided into
three groups: `Ignore misfire policy`, `Run immediately and continue` and
`Discard and wait for next`. Recommendations about using each specific policy
are given below.

### Ignore misfire policy​

This policy is represented by the `MisfireInstruction.IgnoreMisfirePolicy = -1`
constant. It is recommended to use it when it is necessary to ensure that all
trigger firings will be executed even with overdue tasks. For example, the task
A with 2 minutes execution periodicity. Due to lack of Quartz threads or the
scheduler shutdown, the next fire time of task A (`NEXT_FIRE_TIME`) lags 10
minutes from the current time. If execution of all 5 overdue tasks is required,
use the `IgnoreMisfirePolicy` utility.

This policy is recommended to use for triggers that operate with a unique data
at each fire and it is important to perform all trigger fires. For example, the
task B that is executed once per 1 hour and generates the report for the time
period from `PREV_FIRE_TIME` till `PREV_FIRE_TIME + 1`

Applying this policy to triggers that do not operate with unique data may cause
to unnecessary clogging of the scheduler queue and application performance
decrease. For example, the Exchange email synchronization is configured with the
1 minute interval for each Creatio user. An update was performed for 1.5 hours.
After the update, the Quartz will synchronize user mailboxes 90 times before
proceeding with tasks scheduled for the current time. Although it is enough to
perform the delayed synchronization of mailboxes once, and then proceed the task
according to the schedule.

### Run immediately and continue​

This group includes:

- `SimpleTrigger.FireNow`;
- `SimpleTrigger.RescheduleNowWithExistingRepeatCount`;
- `SimpleTrigger.RescheduleNowWithRemainingRepeatCount;`
- `CronTrigger.FireOnceNow`;
- `CalendarIntervalTrigger.FireOnceNow`.

This policies should be used if the overdue task should be executed one time and
as a priority and then execute scheduled tasks. For example, the email
synchronization
(`<user>@<server>_LoadExchangeEmailsProcess_<userId>, SyncImap_<user>@<server>_<userId>`)
or the `RemindingCountersJob` and `SyncWithLDAPProcess` tasks.

For example, email synchronization is configured with the 5 minutes interval for
all users and is fired by the
`<user>@<server>_LoadExchengeEmailProcess_<userId>Trigger` triggers. The update
was performed since 1:30 AM till 2:43 AM. After update, the next fire time for
the `<user>@<server>_LoadExchengeEmailsProcess_<userId>Trigger` triggers will be
changed to 2:43 AM. All overdue tasks will be fired once at 2:43 AM and further
will be fired according to the schedule (2,48 AM, 2:53 AM, 2:58 Am, etc.).

### Discard and wait for next​

This group includes:

- `SimpleTrigger.RescheduleNextWithRemainingCount`;
- `SimpleTrigger.RescheduleNextWithExistingCount`;
- `CronTrigger.DoNothing`;
- `CalendarIntervalTrigger.DoNothing`.

These policies should be applied to the tasks that should be fired strictly at a
specific time. For example the statistics collection launched daily at 3:00 AM
when there is no active users on the website (the `CronTrigger` is used). This
task is resource intensive and time consuming, and it can not be run during
working hours, because this can slow down the work of users. In this case, use
the `CronTrigger.DoNothing` policy. As a result, if the task was not fired, the
next fire will be at 3:00 AM of the next day.

### Quartz configuration​

#### `thread count`​

If the scheduler delays the tasks or if some tasks have not been executed,
increase the number of Quartz threads. For this, set necessary number of threads
in the `Web.config` of the application loader:

    <add key="quartz.threadPool.threadCount" value="5" />

note

The `Web.config` file of the application loader located in the root folder of
the installed Creatio application.

#### `misfireThreshold`​

If the increase in the number of Quartz threads is undesirable (for example, due
to limited resources), the change in the `misfireThreshold` setting in the
`Web.config` file of the application loader can optimize the task execution.

For example, an application with a number of tasks much bigger than a number of
threads. The most of tasks are executed with a small interval (1 minute). The
value of the `misfireThreshold` setting is 1 minute and the number of threads is
3:

    <add key="quartz.jobStore.misfireThreshold" value="60000" />
    <add key="quartz.threadPool.threadCount" value="3" />

For the most of the tasks used the policies from the
`Run immediately and continue` group. This means following. For the most tasks
that have the `MISFIRE_INSTR` not equal "-1" and the `NEXT_FIRE_TIME` less than
the current time for 1 minute (60000 ms) the Quartz will periodically set the
time of the next fire for the current time. This means that the initial order of
the scheduled tasks will be lost because all tasks will have the current time as
the fire time. The probability that Quartz will often process the same tasks and
ignore the other tasks will increase.

The scheduler queue after 15 minutes of working is displayed on the figure.
Tasks that have the `PREV_FIRE_TIME = NULL` never have been executed. There is a
big number of these tasks.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/RecommendedSchedulerSettings/queue_01.png)

Increase the `misfireThreshold` value to 10 minutes (and clear the
`PREV_FIRE_TIME` in `QRTZ_TRIGGERS`):

    <add key="quartz.jobStore.misfireThreshold" value="600000" />;

The scheduler queue after 15 minutes of working:

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/RecommendedSchedulerSettings/queue_02.png)

The number of non-executed tasks is decreased.

Increasing of the value of the `misfireThreshold` will lead to more equal tasks
execution. Almost all jobs from the queue will be executed. Due to lack of
threads, the scheduler does not have time to fire each of the tasks in a minute.
This is displayed in the **Last repeat interval** column that has the value
`NEXT_FIRE_TIME - PREV_FIRE_TIME`, min. However, the scheduler fires each of the
tasks.

#### `batchTriggerAcquisitionMaxCount`​

Increase the `batchTriggerAcquisitionMaxCount` to optimize the scheduler
performance if you do not use the clustered Quartz configuration (one scheduler
node is used).

## Quartz policies for the processing of overdue tasks​

The Quartz has policies common to all types of triggers, and policies that are
specific to a specific type of trigger. All policies used for the
`SimpleTrigger`, `CronTrigger` or `CalendarIntervalTrigger` triggers are listed
below.

Quartz policy| The `MISFIRE_INSTR` value| The
`Terrasoft.Core.Scheduler.AppSchedulerMisfireInstruction` value| Trigger type|
IgnoreMisfirePolicy| -1| IgnoreMisfirePolicy| for all types|
`IgnoreMisfirePolicy` **behavior description** Triggers with the
`IgnoreMisfirePolicy` always will be fired in time. For such triggers, the
Quartz will not update the next fire time (`NEXT_FIRE_TIME`).The Quartz will
fire all overdue tasks as priority, and then return to the initial trigger
schedule. For example, the task with the `SimpleTrigger` was planned for 10
iterations. Initial conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 9` (first fire + 9 iterations)
- `REPEAT_INTERVAL = 0:15`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will try to fire 2 overdue tasks as priority (in 9:00 and 9:15). After that the
Quartz fires the 8 remaining tasks according to the schedule (at 9:30, 9:45,
etc.).| SmartPolicy| 0| SmartPolicy| for all types| `SmartPolicy` **behavior
description** By default is used by Quartz for all types of triggers. According
to the type and configuration of the trigger, the Quartz will select
corresponding policy. The selection algorithm for the Quartz version 2.3.2 is
shown in the pseudo-code below.

    if (TRIGGER_TYPE == 'SIMPLE') // Simple trigger.
        if (REPEAT_COUNT == 0) // Without repeats.
            MISFIRE_INSTR = 1 // SimpleTrigger.FireNow
        else if (REPEAT_COUNT == -1) // COntinious repeating.
            MISFIRE_INSTR = 4 // SimpleTrigger.RescheduleNextWithRemainingCount
        else // The number of repetitions is indicated.
            MISFIRE_INSTR = 2 // SimpleTrigger.RescheduleNowWithExistingRepeatCount
    else if (TRIGGER_TYPE == 'CAL_INT') // CalendarInterval trigger.
        MISFIRE_INSTR = 1 // CalendarIntervalTrigger.FireOnceNow
    else if (TRIGGER_TYPE == 'CRON') // Cron trigger.
        MISFIRE_INSTR = 1 // CronTrigger.FireOnceNow

| SimpleTrigger.FireNow| 1| FireNow| SimpleTrigger| `SimpleTrigger.FireNow`
**behavior description** Applied for the `SimpleTrigger` triggers that have the
`REPEAT_COUNT=0` (triggers fired for one time). If the `REPEAT_COUNT` value is
not "0", then the `SimpleTrigger.RescheduleNowWithRemainingRepeatCount` policy
will be applied.For example, the task planned with the `SimpleTrigger`. Initial
conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 0`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will try to fire the task as priority. As a result, the task will be fired at
9:20 or later.| SimpleTrigger.RescheduleNowWithExistingRepeatCount| 2|
RescheduleNowWithExistingRepeatCount| SimpleTrigger|
`SimpleTrigger.RescheduleNowWithExistingRepeatCount` **behavior description**
Scheduler will try to fire the first overdue task as a priority, All other
triggers will be fired with the `REPEAT_INTERVAL` interval.For example, the task
with the `SimpleTrigger` was planned for 10 iterations. Initial conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 9`
- `REPEAT_INTERVAL = 0:15`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will try to fire first overdue task scheduled for 9:00 (from tasks scheduled on
9:00 and 9:15) at 9:20. The remained 9 tasks will be fired at 9:35, 9:50, etc.
For the `AppScheduler.ScheduleMinutelyJob` methods the behavior of the
`RescheduleNowWithExistingRepeatCount` is similar to the
`RescheduleNowWithRemainingRepeatCount`, and the behavior of the
`RescheduleNextWithRemainingCount` is similar to the
`RescheduleNextWithExistingCount`, because the triggers with the
`REPEAT_COUNT = -1` are used.|
SimpleTrigger.RescheduleNowWithRemainingRepeatCount| 3|
RescheduleNowWithRemainingRepeatCount| SimpleTrigger|
`SimpleTrigger.RescheduleNowWithRemainingRepeatCount` **behavior description**
Scheduler will try to fire the first overdue task as a priority, Other overdue
tasks are ignored. The scheduler fires remained tasks that are not overdue with
the `REPEAT_INTERVAL` interval.For example, the task with the `SimpleTrigger`
was planned for 10 iterations. Initial conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 9`
- `REPEAT_INTERVAL = 0:15`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will try to fire first overdue task (from tasks scheduled on 9:00 and 9:15) at
9:20. The second overdue task will be ignored and other 8 tasks will be fired at
9:35, 9:50, etc.| SimpleTrigger.RescheduleNextWithRemainingCount| 4|
RescheduleNextWithRemainingCount| SimpleTrigger|
`SimpleTrigger.RescheduleNextWithRemainingCount` **behavior description** The
scheduler ignores overdue tasks and waits for the next planned fire of the task.
At the next fire time, the remaining non-overdue tasks will be executed with the
`REPEAT_INTERVAL` interval.For example, the task with the Simple Trigger was
planned for 10 iterations. Initial conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 9`
- `REPEAT_INTERVAL = 0:15`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will fire the rest of 8 non-overdue tasks at 9:30, 9:45, etc.|
SimpleTrigger.RescheduleNextWithExistingCount| 5|
RescheduleNextWithExistingCount| SimpleTrigger|
`SimpleTrigger.RescheduleNextWithExistingCount` **behavior description** The
scheduler will wait for the next launch time and will fire all remained tasks
with the `REPEAT_INTERVAL` interval.For example, the task with the
`SimpleTrigger` was planned for 10 iterations. Initial conditions:

- `START_TIME = 9:00`
- `REPEAT_COUNT = 9`
- `REPEAT_INTERVAL = 0:15`

If the scheduler was disabled from 8:50 till 9:20, then after launch the Quartz
will fire all 10 tasks at 9:30, 9:45, etc.| CronTrigger.FireOnceNow| 1| -|
CronTrigger| `CronTrigger.FireOnceNow` **behavior description** Scheduler will
try to fire the first overdue task as a priority. Other overdue tasks are
ignored. Remained non-overdue tasks are fired by the scheduler according to the
schedule.For example, the task planned with the `CronTrigger`:
`CRON_EXPRESSION = '0 0 9-17 ? * MON-FRI` (from Monday to Friday 9:00 AM – 17:00
PM). If the scheduler was disabled from 8:50 till 10:20, then after launch at
10:20 the Quartz will try to fire first overdue task from two (at 9:00 and
10:00). After that, tasks will be fired at 11:00, 12:00, etc.|
CronTrigger.DoNothing| 2| -| CronTrigger| `CronTrigger.DoNothing` **behavior
description** Scheduler ignores all overdue tasks. Remained non-overdue tasks
will be fired according to the schedule.For example, the task planned with the
`CronTrigger`: `CRON_EXPRESSION = '0 0 9-17 ? * MON-FRI` (from Monday to Friday
9:00 AM – 17:00 PM). If the scheduler was disabled from 8:50 till 10:20, then
after launch the Quartz will start to fire tasks since 11:00 (at 11:00, 12:00,
etc).| CalendarIntervalTrigger.FireOnceNow| 1| -| CalendarIntervalTrigger|
`CalendarIntervalTrigger.FireOnceNow` **behavior description** The behavior is
similar to the `CronTrigger.FireOnceNow`.| CalendarIntervalTrigger.DoNothing| 2|
-| CalendarIntervalTrigger| `CalendarIntervalTrigger.DoNothing` **behavior
description** The behavior is similar to the `CronTrigger.DoNothing`.

---

- Recommendations on scheduler setup
  - Ignore misfire policy
  - Run immediately and continue
  - Discard and wait for next
  - Quartz configuration
- Quartz policies for the processing of overdue tasks
