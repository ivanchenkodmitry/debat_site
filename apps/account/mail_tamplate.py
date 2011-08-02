# -*- coding: utf-8 -*-




SUBJECT = u'Кто-то зарегался!'

DEFAULT_MAIL_BODY = u'Тут человечек хотет в организацию вступить. Надо бы проверить.\n'

def signin_body(**kwargs):
	
	user = kwargs.get('user')
	massage = DEFAULT_MAIL_BODY +  user.username

	us_profile = user.get_profile()
	
	profile =   u"\nЛогин:" + user.username + u"\nИмя:" + us_profile.name + u"\nФамилия:" + us_profile.surname + u"\nОтчество:" + us_profile.middle_name
	massage = DEFAULT_MAIL_BODY + u"А вот и его профаил:\n" + profile
	return massage

	
