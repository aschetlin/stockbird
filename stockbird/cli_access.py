import tweepy
import logging


def cli_access(api):
    print("What would you like to do?\n(1) Update Status (2) DM a user\n")
    operation = int(input("> "))

    if operation == 1:
        print("What would you like to tweet? \n")
        api.update_status(input("> "))

    elif operation == 2:
        print("Who would you like to DM? \n")
        user_name = input("> ")
        user = api.get_user(user_name)

        print("What message would you like to send? \n")
        message = input("> ")
        try:
            api.send_direct_message(user.id, message)

        except tweepy.TweepError.api_code as e:
            if e.api_code == 349:
                print(
                    "You cannot message this user. "
                    "They may be private, have messages disabled, "
                    "or have your account blocked."
                )

            else:
                raise e

    else:
        logging.error("Invalid input.")
        return
