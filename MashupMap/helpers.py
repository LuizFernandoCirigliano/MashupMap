def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
            return instance
        except Exception as e:
            print(e)
            session.rollback()
            return None


def get_or_create_by_id(session, model, instance_id, **kwargs):
    instance = session.query(model).get(instance_id)
    if instance:
        return instance
    else:
        instance = model(id=instance_id, **kwargs)
        session.add(instance)
        session.commit()
        return instance
