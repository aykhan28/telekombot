def build_prompt(user_id, user_input, context):
    system_prompt = (
        "Bir sanal telekom operatörü müşteri temsilcisisin. "
        "Kullanıcıların sorularına dostça, verimli ve çözüm odaklı cevaplar ver. "
        "Tüm cevaplarını aksi belirtilmedikçe Türkçe ver. "
        "Cevaplarının Türkçe olmasına dikkat et.\n"
        "Gerekirse sistem entegrasyonları, durum yönetimi ve hata yönetimi seçenekleri öner.\n"
    )
    return system_prompt + context + f"Kullanıcı: {user_input}\nBot:"
