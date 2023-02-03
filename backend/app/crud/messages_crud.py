from app.db import session
from app.models import MessageContacts, Messages, Users
from sqlalchemy.sql import and_

class MessagesMain:
    def get_chat_history(self, main_user, target_user):
        contact_query = (
            session.query(MessageContacts)
            .where(and_(
                MessageContacts.user_a_id == main_user.id,
                MessageContacts.user_b_id == target_user.id
            ))
            .first()
        )
        if not contact_query:
            contact_query = (
                session.query(MessageContacts)
                .where(and_(
                    MessageContacts.user_a_id == target_user.id,
                    MessageContacts.user_b_id == main_user.id
                ))
                .first()
            )
        if not contact_query:
            #it means there is no contact create a new contact
            contact = MessageContacts(
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
                .order_by(Messages.date).all()
            )
            messages = []
            for message in messages_query:
                messages.append({
                    "id": message.id,
                    "message": message.message,
                    "date": message.date,
                    "sender_id": message.sender_id,
                    "chat_id": message.chat_id
                })
            return messages
            # main_user_messages = []
            # for i in main_user_messages_query:
            #     main_user_messages.append({
            #         "message": i.message,
            #         "date": i.date,
            #         "sender_id": i.sender_id,
            #         "chat_id": i.chat_id
            #     })
            # target_user_messages = []
            # for i in target_user_messages_query:
            #     target_user_messages.append({
            #         "message": i.message,
            #         "date": i.date,
            #         "sender_id": i.sender_id,
            #         "chat_id": i.chat_id
            #     })
            # return {"main_user_messages": main_user_messages, "target_user_messages": target_user_messages}
    
    def get_chat_id(self, main_user, target_user):
        chat_query = (
            session.query(MessageContacts)
            .where(and_(
                MessageContacts.user_a_id == main_user.id,
                MessageContacts.user_b_id == target_user.id
            ))
            .first()
        )
        if not chat_query:
            chat_query = (
                session.query(MessageContacts)
                .where(and_(
                    MessageContacts.user_b_id == main_user.id,
                    MessageContacts.user_a_id == target_user.id
                ))
                .first()
            )
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
        q1 = (
            session.query(MessageContacts)
            .where(MessageContacts.user_a_id == user.id)
        )
        #check as user b
        q2 = (
            session.query(MessageContacts)
            .where(MessageContacts.user_b_id == user.id)
        )

        q = q1.union(q2).all()
        
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
                .order_by(Messages.date.desc())
                .limit(1)
                .first()
            )
            #we need user image and name
            if message_query.sender_id == user.id:
                temp_q = (
                    session.query(MessageContacts)
                    .where(MessageContacts.id == message_query.chat_id)
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

            last_messages.append({
                "user_id": user_query.id,
                "name": user_query.name,
                "username": user_query.username,
                "profile_image": user_query.profile_image,
                "message": message_query.message,
                "sender_id": message_query.sender_id,
                "date": message_query.date
            })
        
        return last_messages