import phonenumbers
from phonenumbers import timezone, geocoder, carrier, NumberParseException, PhoneNumberFormat

def format_number(phone_number):
    international_format = phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
    national_format = phonenumbers.format_number(phone_number, PhoneNumberFormat.NATIONAL)
    return international_format, national_format

def number_type(phone_number):
    number_type = phonenumbers.number_type(phone_number)
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        return "Mobile"
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        return "Fixed Line"
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
        return "Fixed Line or Mobile"
    elif number_type == phonenumbers.PhoneNumberType.TOLL_FREE:
        return "Toll-Free"
    elif number_type == phonenumbers.PhoneNumberType.PREMIUM_RATE:
        return "Premium Rate"
    elif number_type == phonenumbers.PhoneNumberType.SHARED_COST:
        return "Shared Cost"
    elif number_type == phonenumbers.PhoneNumberType.VOIP:
        return "VoIP"
    elif number_type == phonenumbers.PhoneNumberType.PERSONAL_NUMBER:
        return "Personal Number"
    elif number_type == phonenumbers.PhoneNumberType.PAGER:
        return "Pager"
    elif number_type == phonenumbers.PhoneNumberType.UAN:
        return "UAN"
    else:
        return "Unknown"

def check_premium_rate(phone_number):
    number_type = phonenumbers.number_type(phone_number)
    return number_type == phonenumbers.PhoneNumberType.PREMIUM_RATE

def check_validity_for_region(phone_number_str, region_code):
    try:
        phone_number = phonenumbers.parse(phone_number_str, region_code)
        return phonenumbers.is_valid_number_for_region(phone_number, region_code)
    except NumberParseException:
        return False

def detect_formatting_errors(phone_number):
    errors = []
    if not phonenumbers.is_possible_number(phone_number):
        errors.append("Number is not possible.")
    if not phonenumbers.is_valid_number(phone_number):
        errors.append("Number is not valid.")
    return errors

def suggest_correct_format(phone_number):
    formatted_number = phonenumbers.format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
    return formatted_number

def normalize_number(number):
    try:
        phone_number = phonenumbers.parse(number)
        normalized_number = phonenumbers.format_number(phone_number, PhoneNumberFormat.E164)
        return normalized_number
    except NumberParseException:
        return None

def fetch_country_info(country_code):
    # This is a placeholder for fetching detailed country information
    country_info = {
        'US': "United States of America - North America",
        'IN': "India - South Asia",
        'GB': "United Kingdom - Europe",
        'AU': "Australia - Oceania",
        # Add more country codes and information as needed
    }
    return country_info.get(country_code, "Information not available")

def main():
    number = input("Enter phone number with country code: ")
    try:
        normalized_number = normalize_number(number)
        if not normalized_number:
            print("Invalid phone number format.")
            return

        phone_number = phonenumbers.parse(normalized_number)

        # Validate the phone number
        if not phonenumbers.is_valid_number(phone_number):
            print("Invalid phone number.")
            return

        # Check if the phone number is possible
        if not phonenumbers.is_possible_number(phone_number):
            print("Possible number, but not valid.")
            return

        # Formatting the Phone Number
        international_format, national_format = format_number(phone_number)
        print("International Format:", international_format)
        print("National Format:", national_format)

        # Number Type
        phone_number_type = number_type(phone_number)
        print("Number Type:", phone_number_type)

        # Number Length
        number_length = len(str(phone_number.national_number))
        print("Number Length:", number_length)

        # Check for Premium Rate
        is_premium_rate = check_premium_rate(phone_number)
        print("Premium Rate Number:", is_premium_rate)

        # Check Validity for Specific Region
        region_code = input("Enter region code to check number validity (e.g., US, IN): ")
        is_valid_for_region = check_validity_for_region(normalized_number, region_code)
        print(f"Number valid for region '{region_code}':", is_valid_for_region)

        # Detect Formatting Errors
        errors = detect_formatting_errors(phone_number)
        if errors:
            print("Formatting Issues:", ", ".join(errors))
            print("Suggested Format:", suggest_correct_format(phone_number))
        else:
            print("Number appears to be correctly formatted.")

        # Fetch Country-Specific Information
        country_code = str(phone_number.country_code)
        country_info = fetch_country_info(country_code)
        print(f"Country Information for code {country_code}:", country_info)

        # Printing the timezone using the timezone module
        time_zone = timezone.time_zones_for_number(phone_number)
        print("Timezone:", time_zone)

        # Printing the geolocation of the given number using the geocoder module
        location = geocoder.description_for_number(phone_number, "en")
        print("Location:", location)

        # Printing the service provider name using the carrier module
        service_provider = carrier.name_for_number(phone_number, "en")
        print("Service Provider:", service_provider)

        # Compare with another number
        number2 = input("Enter another phone number with country code for comparison: ")
        normalized_number2 = normalize_number(number2)
        if not normalized_number2:
            print("Invalid phone number format for comparison.")
            return

        phone_number2 = phonenumbers.parse(normalized_number2)
        same_region = phonenumbers.region_code_for_number(phone_number) == phonenumbers.region_code_for_number(phone_number2)
        same_service_provider = carrier.name_for_number(phone_number, "en") == carrier.name_for_number(phone_number2, "en")
        print("Both numbers are from the same region:", same_region)
        print("Both numbers have the same service provider:", same_service_provider)

    except NumberParseException as e:
        print(f"Error parsing phone number: {e}")

if __name__ == "__main__":
    main()
