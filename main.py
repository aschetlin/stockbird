import os
import sys

import tweepy

consumer_key = os.getenv("TWT_API_KEY")
consumer_secret = os.getenv("TWT_API_SECRET")
access_token = os.getenv("TWT_ACCESS_TOKEN")
access_secret = os.getenv("TWT_ACCESS_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def main():
    operation = int(input("What would you like to do?\n(1) Update Status (2) DM a user \n"))

    if operation == 1:
        api.update_status(input("What would you like to tweet? \n"))
        return

    elif operation == 2:
        user_name = input("Who would you like to DM? \n")
        user = api.get_user(user_name)

        message = input("What message would you like to send? \n")
        api.send_direct_message(user.id, message)
        return

    else:
        print("Invalid input.")
        return


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
