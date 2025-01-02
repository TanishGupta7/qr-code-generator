import qrcode as qr
from PIL import Image
import re
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Generate a file name based on the domain of the URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[-2]  # Extract the domain name
    return domain + ".png"

def is_valid_url(url):
    """Check if the URL is valid."""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:\S+(?::\S*)?@)?'  # optional user:pass@ part
        r'(?:[A-Za-z0-9.-]+\.[A-Za-z]{2,6})'  # domain
        r'(?:[:\d]{1,5})?'  # optional port
        r'(?:/\S*)?$', re.IGNORECASE)  # path
    return re.match(regex, url) is not None

def is_valid_color(color):
    """Check if the color is valid."""
    try:
        Image.new("RGB", (1, 1), color)  # Try creating a dummy image with the color
        return True
    except ValueError:
        return False

def main():
    print("Welcome to the QR Code Generator!")
    
    # Get the URL from the user
    while True:
        url = input("Enter the URL to generate a QR code: ").strip()
        if is_valid_url(url):
            break
        print("Invalid URL. Please enter a valid URL starting with http or https.")

    # Ask for QR code colors
    while True:
        fill_color = input("Enter the fill color for the QR code (e.g., black, red, blue): ").strip() or "black"
        if is_valid_color(fill_color):
            break
        print("Invalid color. Please enter a valid color name or hex code (e.g., #000000).")

    while True:
        back_color = input("Enter the background color for the QR code (e.g., white, yellow): ").strip() or "white"
        if is_valid_color(back_color):
            break
        print("Invalid color. Please enter a valid color name or hex code (e.g., #FFFFFF).")

    # Generate file name from the URL
    file_name = get_filename_from_url(url)

    # Generate QR code
    print("Generating QR code...")
    qrcode = qr.QRCode(
        version=1,
        error_correction=qr.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qrcode.add_data(url)
    qrcode.make(fit=True)

    # Create and save the QR code image
    try:
        img = qrcode.make_image(fill_color=fill_color, back_color=back_color)
        img.save(file_name)
        print(f"QR code generated and saved as '{file_name}'")
    except Exception as e:
        print(f"An error occurred while generating the QR code: {e}")

if __name__ == "__main__":
    main()
