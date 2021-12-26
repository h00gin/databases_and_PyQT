from sqlalchemy.orm import Session


def get_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()


def get_by_login(db: Session, model):
    # return db.query(model).filter(model.login == login).first()
    return db.query(model).order_by(model.login).all()


def get_by_contacts(db: Session, model, login: str):
    return db.query(model).filter(model.login == login).first()


def get_multi(db: Session, model):
    objects = db.query(model)
    return objects.all()

