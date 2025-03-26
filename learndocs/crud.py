from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    # 获取要更新的用户
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        # 更新用户信息
        db_user.email = user.email
        db_user.hashed_password = user.password + "notreallyhashed"  # 示例中的假加密
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    # 获取要删除的用户
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        # 删除用户
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    # 获取要更新的项目
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        # 更新项目信息
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    # 获取要删除的项目
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        # 删除项目
        db.delete(db_item)
        db.commit()
        return True
    return False
