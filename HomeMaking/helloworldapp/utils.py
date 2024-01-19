def read_emails(start, end):
    with open('C:/Users/user/OneDrive/Desktop/osama/project/data/MailPassPirate_5198.txt', 'r', encoding='utf-8') as file:
        emails = file.readlines()
    return emails[start:end]
