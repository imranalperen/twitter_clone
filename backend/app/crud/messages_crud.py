from app.db import session
from app.models import Chats, Messages, Users
from sqlalchemy.sql import and_, or_

class MessagesMain:
    def get_chat_history(self, main_user, target_user):
        contact_query = (
            session.query(Chats)
            .where(and_(
                Chats.user_a_id == main_user.id,
                Chats.user_b_id == target_user.id
            ))
            .first()
        )
        if not contact_query:
            contact_query = (
                session.query(Chats)
                .where(and_(
                    Chats.user_a_id == target_user.id,
                    Chats.user_b_id == main_user.id
                ))
                .first()
            )
        if not contact_query:
            #it means there is no contact create a new contact
            contact = Chats(
                user_a_id = main_user.id,
                user_b_id = target_user.id
            )
            session.add(contact)
            session.commit()
            return {"status": "new_chat"}
        
        else:
            #if there is contact_query it means there is a chat contact check for messages
            main_user_messages_query = (
                session.query(Messages)
                .where(and_(
                    Messages.sender_id == main_user.id,
                    Messages.chat_id == contact_query.id
                ))
                # .all()
            )
            target_user_messages_query = (
                session.query(Messages)
                .where(and_(
                    Messages.sender_id == target_user.id,
                    Messages.chat_id == contact_query.id
                ))
                # .all()
            )
            messages_query = (
                main_user_messages_query.union(target_user_messages_query)
                .order_by(Messages.date.desc()).all()
            )
            messages = []
            for message in messages_query:
                messages.append({
                    "message": message.message,
                    "date": message.date,
                    "sender_id": message.sender_id,
                    "chat_id": message.chat_id
                })
            return messages
    
    def get_chat_id(self, main_user, target_user):
        chat_query = (
            session.query(Chats)
            .where(and_(
                Chats.user_a_id == main_user.id,
                Chats.user_b_id == target_user.id
            ))
            .first()
        )
        if not chat_query:
            chat_query = (
                session.query(Chats)
                .where(and_(
                    Chats.user_b_id == main_user.id,
                    Chats.user_a_id == target_user.id
                ))
                .first()
            )
        if not chat_query:
            return None
        return chat_query.id

    def post_message(self, user, chat_id, message_body):
        message = Messages(
            sender_id = user.id,
            message = message_body,
            chat_id = chat_id
        )
        session.add(message)
        session.commit()


    def get_user_chat_contacts(self, user):
        #check as user a
        q = (
            session.query(Chats)
            .where(
            or_(
                Chats.user_a_id == user.id,
                Chats.user_b_id == user.id))
            .all()
        )
        
        chat_ids = []
        for i in q:
            chat_ids.append({
                "id": i.id
            })
        # now we can check users and messages which ids = chat_ids
        last_messages = []
        for i in chat_ids:
            message_query = (
                session.query(Messages)
                .where(Messages.chat_id == i["id"])
                #chat id si bu olan sender id si diger taraf olan okunmamis mesajlarin sayisin ibildirim olarak bas
                .order_by(Messages.date.desc())
                .first()
            )
            #we need user image and name
            if message_query.sender_id == user.id:
                temp_q = (
                    session.query(Chats)
                    .where(Chats.id == message_query.chat_id)
                    .first()
                )
                if temp_q.user_a_id == message_query.sender_id:
                    target_user_id = temp_q.user_b_id
                else:
                    target_user_id = temp_q.user_a_id
            else:
                target_user_id = message_query.sender_id
            
            user_query = (
                session.query(Users)
                .where(Users.id == target_user_id)
                .first()
            )

            message_count = (
                session.query(Messages)
                .where(and_(
                    Messages.chat_id == i["id"],
                    Messages.sender_id != user.id,
                    Messages.is_readed == False
                ))
                .count()
            )

            last_messages.append({
                "user_id": user_query.id,
                "name": user_query.name,
                "username": user_query.username,
                "profile_image": user_query.profile_image,
                "message": message_query.message,
                "sender_id": message_query.sender_id,
                "date": message_query.date,
                "message_count": message_count
            })
        
        #sort oldest to newest using bubble sorting alghoritm
        n = len(last_messages)
        for i in range(n):
            for j in range(0, n - i - 1):
                if last_messages[j]["date"] > last_messages[j + 1]["date"]:
                    last_messages[j], last_messages[j + 1] = last_messages[j + 1], last_messages[j]
        
        
        return last_messages

    def mark_as_read(self, user, chat_id):
        q = (
            session.query(Messages)
            .where(and_(
                Messages.chat_id == chat_id,
                Messages.sender_id != user.id
            ))
            .all()
        )
        for i in q:
            if not i.is_readed:
                (
                    session.query(Messages)
                    .where(Messages.id == i.id)
                    .update({
                        "is_readed": True
                    })
                )
                session.commit()
