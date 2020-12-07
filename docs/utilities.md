---
marp: true
paginate: true
---

<style>
h1 {color: #486BD3;
    text-align: center
}

table {
       margin-left: auto;
       width: auto;
       }
</style>

# Summary of functions

- checklogin()
- input_validate()
- register()
- login()
- logout()
- read_message()
- calendar()
- select_menu()
- usr_guide()
- output_file()
- ...


---


# `checklogin()`
🔸 *decorator*

- guset
- patient
- GP
- admin
- redirect to

---

# `input_validate()`
🔸 ❓ *decorator*

Type check + Length check + Domain check

|       What       |
| ---------------- |
| name             |
| email            |
| password         |
| telephone number |
| ...              |

**approaches:**

- `while` + flag variable (T or F)
- `while` + try-except
- *non*-standard library [pyinputplus](https://github.com/asweigart/pyinputplus)

---

# `select_menu(a, *args/**kwargs)`

🔸 *decorator* perhaps

- formatted print (fancy look)
- arguments are choices for users
- always has a reference to `logout()`, `read_message()`...

---

# `register()`

- sql insert

---

# `login()`

- sql select

---

# `logout()`

- command line shortcut 🔶 *decorator*
- empty user_id
- reset user_status

---

# optional `read_message()`

- sql select
- formatted print (fancy look)
- ❓ **how to return to the last page**

---

# `calendar()`

- formatted print
- built-in library [calendar](https://docs.python.org/3/library/calendar.html)

---

A function for GP & admin, not for the patient.
--> 🔶 *GP class static method*

# ~~`search_user(name)`~~

- return the user_id

---


# `usr_guide()`

- help the user know the usage of CLI

---


❓ Shall we have a class for functions which are strongly relevant?

# `class usrhelper()`

register + log-in/out + read_message + ...

---

<style scoped>
h1 {color: grey;
    }
ul {
  margin-right: auto;
  margin-left: auto;
}
</style>

# Global Variables

- usr_id
- (usr_status)

# Other Globally accessible objects

- homepage (it may need an individual .py file)

---

## Extra

# `update_account()`

- sql update
- only admin --> in class

# `output_file()`

- help a user save some information to local space
- pdf, xls, word...

---

*Something might be abstracted from class diagram during coding*

# `sqlhelper()`

```python
Class DatabaseConnection:
    # open & close
    def __init__(self, dbname):
        self.__conn = sqlite3.connect(db_name)
    def __del__(self):
        self.__conn.close()
    # CRUD
    def crud():
        pass
```

---

<style scoped>
h1 {color: red}
</style>

# Coding Guidelines/Tricks/Accumulation

- PEP8

- *A shared document to record while coding*

  1. 【avoid】 `from utilities import *`, since it will pollute the names and make it hard to trace the origin
  2. 【how to】 get rid of too many if/elif statements
  3. 【good tutorials】such as SQLite tutorial

# Tests

- unit test
- test case