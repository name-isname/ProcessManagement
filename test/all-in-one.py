# define a tabel about student in database
# create student table(
#     id int primary key, name varchar(255), age int, gender varchar(255) )



from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy.orm import mapped_column,Mapped,relationship # 导入映射列
from sqlalchemy import Integer,String,ForeignKey # 导入整数类型和字符串类型
from sqlalchemy import select

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(255))
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    class_in : Mapped["Class"] = relationship(back_populates="studnts")


    def __repr__(self) -> str:
        return f"Student(id={self.id!r}, name={self.name!r}, age={self.age!r}, gender={self.gender!r})"

class Class(Base):
    __tablename__ = "classes"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    studnts : Mapped[list["Student"]] = relationship(back_populates="class_in")


    def __repr__(self) -> str:
        return f"Class(id={self.id!r}, name={self.name!r}, studnts={self.studnts!r})"

from sqlalchemy import create_engine
engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
SessionGenerated = sessionmaker(bind=engine)

db = SessionGenerated()

def get_student_by_name(name: str, db: SessionGenerated):
    reslut = db.execute(select(Student).where(Student.name == name)).scalars().first()
    if reslut is None:
        return 0
    else:
        return reslut

def get_all_student(db: SessionGenerated):
    return db.execute(select(Student)).scalars().all()

def print_all(db: SessionGenerated,function:callable):
    print("----------------")
    # print(function(db))
    for student in function(db):
        print(student)

def get_all_name(db: SessionGenerated):
    return db.execute(select(Student.name)).scalars().all()

def add_student(name: str, age: int, gender: str,class_id: int, db: SessionGenerated):
    student = Student(name=name, age=age, gender=gender ,class_id=class_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def create_student(db: SessionGenerated):
    name, age, gender = ["张三", 20, "男"]
    add_student(name, age, gender, db)

def create_student_4times(db: SessionGenerated):
    add_student("张三", 20, "男",1, db)
    add_student("李四", 21, "男",1, db)
    add_student("王五", 22, "男",1, db)
    add_student("赵六", 23, "男",1, db)


def get_student_info():
    name = input("请输入姓名:")
    age = int(input("请输入年龄:"))
    gender = input("请输入性别:")
    return name, age, gender

def create_class():
    class1 = Class(name="一班")
    db.add(class1)
    db.commit()
    db.refresh(class1)
    return class1

def get_all_class(db: SessionGenerated):
    return db.execute(select(Class)).scalars().all()

with db:
    #print_all(db,get_all_class)
    #create_student_4times(db)
    #print_all(db,get_all_student)
    stu = get_student_by_name("张三", db)
    print(stu.class_in.studnts[0].class_in)