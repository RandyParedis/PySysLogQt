## Filtering of Messages

Often, one would like to obtain information about specific messages. This can
be done by filtering the messages. In the "_Filter_" box, you can provide an
expression, indicative of the filter you would like.

These filters are case-insensitive, unless when searching for a string.

#### Expressions
Each filter consists of a set of boolean expressions, which can be combined
using the `and` and `or` operators. An expression can be negated
by adding the unary `not` operator to the front.

The expressions are solved from left to right. If parentheses are used to
group multiple expressions together, all groups are solved first.

In total, there are eight binary operators and one unary operator, as defined
in the table below. The first column defines the name for the operator, the
second identifies how the operator works and the third provides the meaning.

| Operator | Syntax | Sematics |
|:---:|:---:|:---|
| Less Than | `a < b` or `a lt b` | Yields true if `a` is less than `b` |
| Less Than or Equals | `a <= b` or `a le b` | Yields true if `a` is less than or equal to `b` |
| Greater Than | `a > b` or `a gt b` | Yields true if `a` is greater than `b` |
| Greater Than or Equals | `a >= b` or `a ge b` | Yields true if `a` is greater than or equal to `b` |
| Equals | `a == b` or `a eq b` or `a is b` | Yields true if `a` is equal to `b` |
| Not Equals | `a != b` or `a ne b` | Yields true if `a` is not equal to `b` |
| Not Equals | `a != b` or `a ne b` | Yields true if `a` is not equal to `b` |
| Containment | `a in b` | Yields true if `a` can be found in `b`. |
| And | `a and b` or `a && b` | Yields true if both `a` and `b` are true. |
| Or | `a or b` or <code>a &#124;&#124; b</code> | Yields true if either `a` or `b` is true. |
| Not | `not a` or `!a` | Negates the boolean value of `a`. |

#### Column Names
Obviously, it would make sense that we can select records based on column
values. To select a column, just type the column name (case insensitive).
E.g. selecting all records where the `ID` value lies between 0 and 10 can be
written as: `0 < id and id < 10`.

Note that `FACILITY` and `LEVEL` are evaluated numerically.

#### Strings and Numbers
You can use numbers in the filter box, following a normal format: they can be
negated, may have as many numbers behind the decimal as desired, but they
cannot start with a 0, _unless_ it is the only character before the decimal
place; i.e. `012.5` is invalid, use `12.5` instead. Furthermore, when using a
decimal, there *must* be a number before the decimal; i.e. `.156` is invalid,
use `0.156` instead. The full regular expression that matches numbers is:
`-?([1-9][0-9]*|0)(\.[0-9]*)?`

Strings can be used as well, as long as they are encapsulated in double quotes.
The `in`-operator can be used to check substrings.

#### Special Keywords
Specific colums might require specific values. These keywords are summarized
below. They are all case-insensitive.

| Keyword | Meaning |
| :---:|:---|
| `today` | Today's timestamp (ignoring the time). |
| `now` | The current time, ignoring the microseconds. |
| `emergency` or `emerg` | The numerical value of the `EMERGENCY` level. |
| `alert` | The numerical value of the `ALERT` level. |
| `critical` | The numerical value of the `CRITICAL` level. |
| `error` | The numerical value of the `ERROR` level. |
| `warning` | The numerical value of the `WARNING` level. |
| `notice` | The numerical value of the `NOTICE` level. |
| `info` or `information` | The numerical value of the `INFO` level. |
| `debug` | The numerical value of the `DEBUG` level. |
| `kernel` | The numerical value of the `Kernel` facility. |
| `userlevel` | The numerical value of the `User-Level` facility. |
| `mailsystem` | The numerical value of the `Mail System` facility. |
| `systemdaemons` | The numerical value of the `System Daemons` facility. |
| `security1` | The numerical value of the `Security 1` facility. |
| `internal` | The numerical value of the `Internal` facility. |
| `lineprinter` | The numerical value of the `Line Printer` facility. |
| `networknews` | The numerical value of the `Network News` facility. |
| `uucp` | The numerical value of the `UUCP` facility. |
| `clockdaemon` | The numerical value of the `Clock Daemon` facility. |
| `security2` | The numerical value of the `Security 2` facility. |
| `ftpdaemon` | The numerical value of the `FTP Daemon` facility. |
| `ntp` | The numerical value of the `NTP` facility. |
| `logaudit` | The numerical value of the `Log Audit` facility. |
| `logalert` | The numerical value of the `Log Alert` facility. |
| `scheduling` | The numerical value of the `Scheduling` facility. |
| `local0` | The numerical value of the `Local 0` facility. |
| `local1` | The numerical value of the `Local 1` facility. |
| `local2` | The numerical value of the `Local 2` facility. |
| `local3` | The numerical value of the `Local 3` facility. |
| `local4` | The numerical value of the `Local 4` facility. |
| `local5` | The numerical value of the `Local 5` facility. |
| `local6` | The numerical value of the `Local 6` facility. |
| `local7` | The numerical value of the `Local 7` facility. |
