import environs

env = environs.Env()
env.read_env()


class Settings:
    bot_token = env.str("BOT_TOKEN", "8620751527:AAGolJy8SUxrBLNYyXHJZ-Mw5okvrWiA5I8")
    bot_user_redis = env.bool("BOT_USE_REDIS", default=False)
    tg_api_server_url = env.str("TG_API_SERVER_URL", default="https://api.telegram.org")
    admins_ids = env.list("ADMINS_IDS", default=[7892805795])

    db_name = env.str("DB_NAME", "media_1rb3")
    db_user = env.str("POSTGRES_USER", "media_1rb3_user")
    db_password = env.str("POSTGRES_PASSWORD", "2oUMuOnjKhiDpDOid0SW5TfaBpiQTowQ")
    db_host = env.str("POSTGRES_HOST", "dpg-d7hrc1nlk1mc739h148g-a")
    db_port = env.str("POSTGRES_PORT", "5432")

    redis_host = env.str("REDIS_HOST", default="localhost")
    redis_db_name = env.str("REDIS_DB", default="0")

    selenium_url = env.str("SELENIUM_REMOTE_URL", default="http://localhost:4444/wd/hub")

    lastfm_api_key = env.str("LASTFM_API_KEY", default="f25528f2546d239c7922e8794225478b")
