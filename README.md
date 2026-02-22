# 📚 Book Store API
RESTful API for book store built using **Django REST Framework**.
This project implements full cycle of managing books and orders and users authorization.

---

## 🛠 Technology stack
| **Category** | **Technology** |
| :--- | :--- |
|**Backend**| Python 3.12+, Django 4.2+, DRF |
| **Authentication** | JWT (SimpleJWT), Djoser |
| **Databases** | PostgreSQL, Redis (for caching) |
| **DevOps** | Docker, WSL 2 (Ubuntu) |
| **Testing** | APITestCase |

---

## API Endpoints

**Authentication (Djoser+JWT)**
| **Method** | **Endpoint** | **Description** |
| :--- | :--- | :--- |
| **POST** | /api/auth/users/ | Register new user |
| **POST** | /api/auth/jwt/create/ | Login (get tokens) |
| **GET** | /api/auth/users/me/ | Get current user |

**Books**
| **Method** | **Endpoint** | **Description** | **Permissions** |
| :--- | :--- | :--- |
| **GET** | /api/books/ | List all books | AllowAny |
| **GET** | /api/books/{book_id} | Get book by ID | AllowAny |
| **POST** | /api/books/ | Add new book | Admin |
| **PUT** | /api/books/{book_id} | Edit book | Admin |
| **DELETE** | /api/books/{book_id} | Delete book | Admin |

**Orders**
| **Method** | **Endpoint** | **Description** | **Permissions** |
| :--- | :--- | :--- |
| **GET** | /api/orders/ | List all orders | Admin |
| **GET** | /api/orders/ | List users orders | Authenticated |
| **GET** | /api/orders/{id} | Get order details | Admin/Owner |
| **POST** | /api/orders/ | Create new order | Authenticated |

**Users**
| **Method** | **Endpoint** | | **Description** | **Permissions** |
| :--- | :--- | :--- |
| **GET** | /api/users/ | List all users | Admin |
| **GET** | /api/users/{user_id}/ | View user details | Admin |
| **DELETE** | /api/users/{user_Id}/ | Delete user | Admin |

---

## Testing
Project is provided with some unit-tests for orders logic and checking permissions.

To start tests:
python manage.py test

---

## Performance optimization 

## Throttling

To provide stable work, I implemented Throttling

| **Request Type**  | **Limit** | **Description** |
| :--- | :--- | :--- |
| **Anonymous requests** | 3 req/min |  Limit for unauthorized users |
| **Orders** | 4 req/min | Protect logic of creating orders |
| **Books** | 5 req/min | Limit for viewing books |

## Caching (Redis)

We cache data that is read frequently, but written infrequently and static but essential to reduce the load on the database. 
**Endpoints:** /api/books/, /api/orders/
