import sqlite3
from loguru import logger
from conf_init import check_superadmin



def create_db():
    logger.info('Cheching db')
    try:
        db = sqlite3.connect('users.db')
        db.execute('''CREATE TABLE if not exists users
        (joining_date datetime, Fname TEXT, username TEXT, id integer PRIMARY KEY, language_code TEXT,
         is_premium BOOL, admin BOOL, messages integer)''')
        logger.debug('Users created')
    except sqlite3.OperationalError:
        logger.debug('Users already exists')
    db.close()



def add_user(message):
    logger.info('Adding user')
    db = sqlite3.connect('users.db')
    db.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)',
               (message.date, message.from_user.full_name, message.from_user.mention,
               message.from_user.id, message.from_user.language_code,
               message.from_user.is_premium, False, 1))
    db.commit()
    logger.debug('User added')
    db.close()



def check_user(message):
    db = sqlite3.connect('users.db')
    if type(message) != int and type(message) != str:
        user = db.execute('SELECT * FROM users WHERE id=?', (message.from_user.id,)).fetchall()
        logger.debug('Checking user {}'.format(message.from_user.id))
    else:
        user = db.execute('SELECT * FROM users WHERE id=?', (message,)).fetchall()
        logger.info('Checking user {}'.format(message))
    if user == []:
        logger.debug('User not found')
        return False
    else:
        logger.debug('User found')
        return True
    db.close()



def update_user_info(message):
    logger.info('Updating user info')
    db = sqlite3.connect('users.db')
    db.execute('UPDATE users SET Fname=?, username=?, language_code=?, is_premium=? WHERE id=?',
               (message.from_user.full_name, message.from_user.mention, message.from_user.language_code,
                message.from_user.is_premium, message.from_user.id))
    db.commit()
    logger.debug('User info updated')
    db.close()



def add_message(message):
    logger.debug('Adding new message to {}'.format(message.from_user.id))
    db = sqlite3.connect('users.db')
    db.execute('UPDATE users SET messages=messages+1 WHERE id=?', (message.from_user.id,))
    db.commit()
    logger.debug('Message added, total messages: {}'.format(db.execute('SELECT messages FROM users WHERE id=?',
                                                                       (message.from_user.id,)).fetchall()[0][0]))
    db.close()



def user_info(message):
    if check_user(message) == False:
        add_user(message)
    else:
        add_message(message)
    if message.reply_to_message is None and len(message.text.split()) == 1:         # If no reply and no id
        user_id = message.from_user.id
    elif message.reply_to_message is not None and len(message.text.split()) == 1:   # If reply and no id
        if check_user(message.reply_to_message) == False:
            add_user(message.reply_to_message)
        user_id = message.reply_to_message.from_user.id
    elif len(message.text.split()) == 2:                                            # If via user id
        user_id = int(message.text.split()[1])
        if check_user(user_id) == False:
            logger.debug('User {} not found'.format(user_id))
            return ('User not found')
    else:
        return ('Wrong command')

    if user_id:
        db = sqlite3.connect('users.db')
        logger.info(f'Getting user {user_id} info')
        user = db.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchall()

        premium = 'Yes' if user[0][5] else 'No'
        if check_superadmin(int(user_id)):
            admin_status = 'Superadmin'
            admin = 'Yes'
        elif user[0][6]:
            admin_status = 'Admin'
            admin = 'Yes'
        else:
            admin_status = 'Admin'
            admin = 'No'

        logger.debug('User info: {}'.format(user))
        db.close()
        return f"""<b>Joining date to bot:</b> {user[0][0]}
    <b>Full name:</b> {user[0][1]}
    <b>Username:</b> {user[0][2]}
    <b>Id:</b> {user[0][3]}
    <b>Language:</b> {user[0][4]}
    <b>Premium:</b> {premium}
    <b>{admin_status}:</b> {admin}
    <b>Messages:</b> {user[0][7]}"""



def check_admin(user_id:int):
    logger.debug('Checking admin status for {}'.format(user_id))
    db = sqlite3.connect('users.db')
    admin = db.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchall()
    db.close()
    if admin[0][0] == 0:
        logger.debug('User {} is not admin'.format(user_id))
        return False
    else:
        logger.debug('User {} is admin'.format(user_id))
        return True



def add_admin(message):
    logger.debug('Adding user to admins')
    try:
        if message.reply_to_message.from_user.id == 5023608271:
            logger.debug('trying to add bot to admin')
        return 'You can\'t add me to admins'
    except:
        pass
    if check_user(message) == False:
        logger.debug('{} is not in database'.format(message.from_user.id))
        add_user(message)
    else:
        add_message(message)
    if len(message.text.split()) == 2:
        logger.debug("mod user_id")
        user_id = int(message.text.split()[1])
        if check_user(user_id) == False:
            return 'User {} not found'.format(user_id)
        logger.info('Adding {} to admins via user_id'.format(user_id))
    elif message.reply_to_message is not None:
        logger.debug("mod reply")
        if check_user(message.reply_to_message) == False:
            logger.debug('{} is not in database'.format(message.reply_to_message.from_user.id))
            add_user(message.reply_to_message)
        user_id = message.reply_to_message.from_user.id
        logger.info('Adding {} to admins via reply'.format(user_id))
    else:
        logger.debug("no reply or id error")
        return 'Reply to user or use /addadmin user_id'
    if user_id:
        db = sqlite3.connect('users.db')
        fname = db.execute('SELECT fname FROM users WHERE id=?', (user_id,)).fetchall()[0][0]
        if check_superadmin(message.from_user.id) or check_admin(message.from_user.id): user1 = True
        else: user1 = False
        if check_superadmin(user_id) or check_admin(user_id): user2 = True
        else: user2 = False

        if user1 == False:
            logger.info('{} is not admin'.format(user_id))
            db.close()
            return 'You are not admin'
        elif user1 == True and user2 == True:
            logger.info('{} is already admin'.format(user_id))
            db.close()
            return f'{fname} is already admin'
        elif user1 == True and user2 == False:
            db.execute('UPDATE users SET admin=? WHERE id=?', (True, int(user_id),))
            logger.info('{} added to admins'.format(user_id))
            db.commit()
            db.close()
            return f'{fname} added to admins'



def remove_admin(message):
    logger.debug('Removing user from admins')
    try:
        if message.reply_to_message.from_user.id == 5023608271:
            logger.debug('Trying to remove bot from admins')
        return 'You can\'t delete me from admins'
    except:
        pass
    if check_user(message) == False:
        logger.debug('{} is not in database'.format(message.from_user.id))
        add_user(message)
    else:
        add_message(message)

    if len(message.text.split()) == 2:
        logger.debug("mod user_id")
        user_id = int(message.text.split()[1])
        if check_user(user_id) == False:
            return 'User {} not found'.format(user_id)
        else:
            logger.info('Removing {} from admins via user_id'.format(user_id))
            db = sqlite3.connect('users.db')
            fname = db.execute('SELECT fname FROM users WHERE id=?', (user_id,)).fetchall()[0][0]
    elif message.reply_to_message is not None and len(message.text.split()) == 1:
        logger.debug("mod reply")
        if check_user(message.reply_to_message) == False:
            logger.debug('{} is not in database'.format(message.reply_to_message.from_user.id))
            add_user(message.reply_to_message)
        user_id = message.reply_to_message.from_user.id
        logger.info('Removing {} from admins via reply'.format(user_id))
    else:
        logger.debug("no reply error")
        return 'Reply to user or use /removeadmin user_id'

    if user_id:
        if check_superadmin(message.from_user.id) or check_admin(message.from_user.id): user1 = True
        else: user1 = False
        if check_superadmin(user_id) or check_admin(user_id): user2 = True
        else: user2 = False
        if user1 == False:
            logger.info('{} is not admin'.format(user_id))
            db.close()
            return 'You are not admin'
        elif user1 == True and user2 == True:
            db.execute('UPDATE users SET admin=? WHERE id=?', (False, int(user_id),))
            logger.info('{} removed from admins'.format(user_id))
            db.commit()
            db.close()
            return f'{fname} removed from admins'
        elif user1 == True and user2 == False:
            logger.info('{} is just user'.format(user_id))
            db.close()
            return f'{fname} is just user'
        elif (check_admin(message.from_user.id) == True and check_superadmin(message.from_user.id) == False) and check_superadmin(user_id) == True:
            logger.info('{} tried to delete superadmin'.format(message.from_user.id))
            db.execute('UPDATE users SET admin=? WHERE id=?', (False, int(message.from_user.id),))
            db.commit()
            db.close()
            return """You can\'t delete superadmin and you are not admin anymore"""
        elif check_superadmin(message.from_user.id) == True and check_superadmin(user_id) == True:
            logger.info('Superadmin {} tried to delete superadmin'.format(message.from_user.id))
            db.close()
            return 'Why are you tried to delete superadmin?'



def admin_list():
    db = sqlite3.connect('users.db')
    admins = db.execute('SELECT * FROM users WHERE admin=?', (True,)).fetchall()
    db.close()
    admin_list = ''
    for admin in admins:
        admin_list += f'{admin[1]} - {admin[3]}\n'
    return admin_list