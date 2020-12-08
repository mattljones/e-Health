# COMP0066_Coursework

- [COMP0066_Coursework](#comp0066_coursework)
  - [Documentaion](#documentaion)
  - [Database](#database)
    - [Current status](#current-status)
    - [Dummy data](#dummy-data)
    - [Users](#users)
      - [Admin](#admin)
      - [GP](#gp)
      - [Patient](#patient)
## Documentaion
- [Developing Guidence](/docs/developing.md)

## Database

### Current status 
**Done**  
- [x] Set up sqlite db
- [x] Updated ER diagram  

**Todo**  
- [ ] Need to put more thinking around the whole foreign keys relationship.
- [ ] Dummy data (especially for availability)
- [ ] Set indexes

### Dummy data
We are currently developing some dummy data.

[Link to NHS Drug List](https://www.england.nhs.uk/wp-content/uploads/2017/04/NHS-England-drugs-list-v15-2020-2021.pdf)

### Users
#### Admin

Admin is user No. 1 with user_id = 1, please see all details below:

| user\_id | user\_first\_name | user\_last\_name | user\_gender | user\_brith\_date | user\_email | user\_password | user\_registration\_date | user\_type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Admin | Admin | not known | 2020-01-01 | admin@email.com | admin | 2020-12-03 22:40:21 | admin |


#### GP

#### Patient
