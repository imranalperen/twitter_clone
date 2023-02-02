from app.db import session
from app.models import MessageContacts, Messages, Users
from sqlalchemy.sql import and_

class MessagesMain:
    def get_chat_history(self, main_user, target_user):
        # if main_user.id % 2 == 0:
        #     user_a = main_user.id
        #     user_b = target_user["id"]
        #     contact_query = (
        #         session.query(MessageContacts)
        #         .where(MessageContacts.user_a_id == user_a)
        #         .first()
        #     )
        # else:
        #     user_b = main_user.id
        #     user_a = target_user["id"]
        #     contact_query = (
        #         session.query(MessageContacts)
        #         .where(MessageContacts.user_a_id == user_a)
        #         .first()
        #     )
        contact_query = (
            session.query(MessageContacts)
            .where(and_(
                MessageContacts.user_a_id == main_user.id,
                MessageContacts.user_b_id == target_user["id"]
            ))
            .first()
        )
        if not contact_query:
            contact_query = (
                session.query(MessageContacts)
                .where(and_(
                    MessageContacts.user_a_id == target_user["id"],
                    MessageContacts.user_b_id == main_user.id
                ))
                .first()
            )
        if not contact_query:
            #it means there is no contact create a new contact
            contact = MessageContacts(
                user_a_id = main_user.id,
                user_b_id = target_user["id"]
            )
            session.add(contact)
            session.commit()
            return {"status": "new_chat"}
        
        else:
            #if there is q.id it means there is a chat contact check for messages
            main_user_messages_query = (
                session.query(Messages)
                .where(and_(
                    Messages.sender_id == main_user.id,
                    Messages.chat_id == contact_query.id
                ))
                .order_by(Messages.date.desc())
                .all()
            )
            target_user_messages_query = (
                session.query(Messages)
                .where(and_(
                    Messages.sender_id == target_user["id"],
                    Messages.chat_id == contact_query.id
                ))
                .order_by(Messages.date.desc())
                .all()
            )

            main_user_messages = []
            for i in main_user_messages_query:
                main_user_messages.append({
                    "message": i.message,
                    "date": i.date,
                    "sender_id": i.sender_id,
                    "chat_id": i.chat_id
                })
            target_user_messages = []
            for i in target_user_messages_query:
                target_user_messages.append({
                    "message": i.message,
                    "date": i.date,
                    "sender_id": i.sender_id,
                    "chat_id": i.chat_id
                })
            return {"main_user_messages": main_user_messages, "target_user_messages": target_user_messages}
            



