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
