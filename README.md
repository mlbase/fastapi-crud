# fastApi 학습노트

## project 환경설정

---

- requirements.txt ⇒ pip 의존성 관리
- ddl.sql ⇒ mysql database table 생성
- .env ⇒ db secrete key(username, password 등등) gitignore로 git에는 따로 없음
- 사용환경설정#
    - python : 3.10
    - database: mysql
    - ide: pycharm community version
    - 가상환경: miniconda
    - 주요 의존성: fastapi, pydantic, sqlalchemy

## error memo

---

`Depends()` 사용시 주의 사항

- method로 의존성을 주입할 때, 반드시 `function_name()` 이 아닌 `function_name` 으로 주입을 해줘야한다.(아마도 메모리 주소를 직접 참조하는 듯하다….)

---

### pydantic을 사용하지 않는 parameter의 경우 의존성 주입을 해줘야 restdocs가 나오고 api가 동작한다.

---

```python
@router.get("/me", response_model=schema.User)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
) -> Any:
```

위함수에서 schema의 경우 pydantic의 base 모델을 상속받아 pydantic 의존성을 주입 받았지만, entity인 model의 경우 pydantic에 대한 의존성이 존재하지 않는다. 이런경우 fastapi의 `Depends()` 메서드를 이용해서 의존성을 주입해줄 method가 필요하다.

---

## python을 사용할 때 객체를 constructing 하는 경우 parameter 의 이름을 명시해주기

---

```python
def get_current_user(db: Session = Depends(get_db)) -> model.User:
    user = crud.user.get_by_email(session=db, email="test@test.com")
    if not user:
        user_in = UserCreate.parse_obj({'email': 'test@test.com', 'password': '1234', 'full_name': 'testing..'})
        user = crud.user.create(session=db, obj_in=user_in)

    return user
```

- 해당 argument의 해당하는 parameter을 `db=db` 와 같이 1:1로 대응시켜줘야 argument error 가 발생하지 않는다.

---

## pip freeze 를 사용할 경우 `pip list --format=freeze > requirements.txt` 로 사용

---

## debgging 사용하기

```python
if __name__ == "__main__":
    app.include_router(api_router, prefix="/v1")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## SessionLocal vs engine

- orm 을 사용하는 경우에는 sessionLocal 사용하기
- direct query를 직접 querying 하는 경우에는 engine

```python
engine = create_engine(f"{SQLALCHEMY_DATABASE_URL}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## entity 객체 생성

- jpa 처럼 직접 table을 만들어주지는 않는다…

```python
m typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str
    __table_args__ = {'extend_existing': True}
    #Generate __tablename__ automatically
    def __tablename__(self) -> str:
        return self.__name__.lower()
```

Base class를 생성하고 이 Base를 entity class에 상속한다.

```python
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from config.base_class import Base

if TYPE_CHECKING:
    from .item import Item

class User(Base):
    __tablename__ = "api_user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
```

relationship에 해당하는 연관관계는 추후에 다루기로 한다.

---

## 모든 data 응답은 기본적으로 pydantic class를 기반으로 한다.

- entity를 직접참조하는 것도 당연히 문제지만, 기본적으로 sqlAlchemy의 `as_declarative` 클래스는 fastapi 가 인식하는 request/response type이 아니다.
- java에서 dto를 사용하는 것과 유사하게 fastapi에서는 pydantic class를 이용하여 data를 전달한다.(dto 같은 느낌)

---