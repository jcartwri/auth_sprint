from user_agents import parse


def parsing(ua_string: str) -> str:
    user_agent = parse(ua_string)
    info_about_device = {user_agent.is_mobile: 'mobile',
                         user_agent.is_tablet: 'tablet',
                         user_agent.is_pc: 'web',
                         user_agent.is_bot: 'bot'}
    try:
        return info_about_device[True]
    except KeyError:
        return 'test'
