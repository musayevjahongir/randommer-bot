from settings import URL, API_KEY, cart_msg
from datetime import datetime
import requests
from time import sleep
from random import choice
from randomer import card, finance, misc, name, phone, social_number,  text1


welcome_msg =""""Hello and welcome to Randommer Bot!

🎉 Get ready for a diverse range of randomness with our exciting features. Here's a quick guide on how to use this bot:

1. /start: Use this command to receive a warm welcome message and get instructions on how to interact with the bot.

2. /card: Feeling lucky? Use this command to draw a random card and see what fortune it holds for you.

3. /finance: Looking for some crypto randomness? Type this command to get a random crypto address.

4. /misc: Explore the richness of various cultures! Use this command to receive information on 5 randomly selected cultures.

5. /name: Need a name on the spot? Type this command for a completely random full name.

6. /phone: If you're in need of phone numbers, use this command to get 5 randomly generated Uzbekistan phone numbers.

7. /social_number: Curious about social numbers? Use this command to get a randomly generated social number.

8. /text: Want some Lorem Ipsum text? Type this command to receive 20 words of normal Lorem Ipsum text.

"""
def get_last_update(url: str) -> dict:
    endpoint = '/getUpdates'
    url += endpoint # https://api.telegram.org/bot{TOKEN}/getUpdates

    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        if len(result) == 0:
            return 404
        last_update = result[-1]
        return last_update

    return response.status_code

def send_message(url: str, chat_id: str, text: str, mode=False):
    endpoint = '/sendMessage'
    url += endpoint

    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if mode:
        payload["parse_mode"] = "HTML"

    requests.get(url, params=payload)

def main(url: str):
    last_update_id = -1
    
    while True:
        current_update = get_last_update(url)
        if current_update['update_id'] != last_update_id:
            user = current_update['message']['from']
            text = current_update['message'].get('text')

            if text is None:
                send_message(url, user['id'], 'send a message.')

            elif text == '/start':
                send_message(url, user['id'], welcome_msg)

            elif text == '/card':
                c=card.Card()
                cart_data = c.get_card(api_key=API_KEY)
                date_object = datetime.fromisoformat(cart_data['date'])
                msg = cart_msg.format(
                    bank=cart_data['type'],
                    fullname=cart_data['fullName'],
                    number=cart_data['cardNumber'],
                    pin=cart_data['pin'],
                    cvv=cart_data['cvv'],
                    date=date_object.strftime('%Y-%m-%d')
                    )
                send_message(url, user['id'], msg, mode=True)
            elif text == '/finance':
                finance_=finance.Finance()
                finance1 = finance_.get_crypto_address_types(API_KEY)
                send_message(url, user['id'], choice(finance1))

            elif text == "/misc":
                misc_=misc.Misc()
                misc1=choice([i["code"] for i in misc_.get_cultures(API_KEY)])
                misc2=misc_.get_random_address(API_KEY, 5, misc1)
                send_message(url, user["id"], "\n".join(misc2))

            elif text == "/name":
                name_ = name.Name()
                name1=name_.get_name(API_KEY, "fullname", 1)
                send_message(url, user["id"], name1)
        
            elif text == "/phone":
                phone_=phone.Phone()
                phone1=phone_.generate(API_KEY, "uz", 5)

                send_message(url, user["id"], "\n".join(phone1))

            elif text == "/social_number":
                number=social_number.SocialNumber()
                number1=number.get_SocialNumber(API_KEY)
                send_message(url, user["id"], number1)
            
            elif text == "/text":
                text_ = text1.Text()
                text_1 = text_.generate_LoremIpsum(API_KEY, "normal", "words", 20)
                send_message(url, user["id"], text_1)
            
            else:
                send_message(url, user["id"], "Error massage")

        last_update_id = current_update['update_id']

        sleep(0.5)

main(URL)
