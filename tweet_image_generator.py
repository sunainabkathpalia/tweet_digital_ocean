from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from textwrap import wrap
import datetime
import warnings

# font
font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
font_HelveticaNeue_ttc = len(
    [s for s in font_list if "HelveticaNeue.ttc" in s]) > 0
font_Arial_ttf = len([s for s in font_list if "Arial.ttf" in s]) > 0
if font_HelveticaNeue_ttc:
    font = font_manager.FontProperties(
        family='Helvetica Neue', weight='regular')
    font_regular_file = font_manager.findfont(font)
    font = font_manager.FontProperties(family='Helvetica Neue', weight='bold')
    font_bold_file = font_manager.findfont(font)
elif font_Arial_ttf:
    font = font_manager.FontProperties(family='Arial', weight='regular')
    font_regular_file = font_manager.findfont(font)
    font = font_manager.FontProperties(family='Arial', weight='bold')
    font_bold_file = font_manager.findfont(font)
else:
    font = font_manager.FontProperties(family='sans-serif', weight='regular')
    font_regular_file = font_manager.findfont(font)
    font = font_manager.FontProperties(family='sans-serif', weight='bold')
    font_bold_file = font_manager.findfont(font)
if font_regular_file[-4:] == '.ttc':
    font_author_name = ImageFont.truetype(font_bold_file, size=35, index=1)
    font_author_tag = ImageFont.truetype(font_regular_file, size=25, index=0)
    font_text = ImageFont.truetype(font_regular_file, size=35, index=0)
    font_time_date = ImageFont.truetype(font_regular_file, size=24, index=0)
    font_reaction_regular = ImageFont.truetype(font_regular_file, size=30, index=0)
    font_reaction_bold = ImageFont.truetype(font_bold_file, size=30, index=1)
    font_quote_author_name = ImageFont.truetype(font_bold_file, size=27, index=1)
    font_quote_author_tag = ImageFont.truetype(font_regular_file, size=27, index=0)
    font_quote_text = ImageFont.truetype(font_regular_file, size=25, index=0)
    font_reply_author_name = ImageFont.truetype(font_bold_file, size=27, index=1)
    font_reply_author_tag = ImageFont.truetype(font_regular_file, size=27, index=0)
    font_reply_text = ImageFont.truetype(font_regular_file, size=25, index=0)
else:
    font_author_name = ImageFont.truetype(font_bold_file, size=35)
    font_author_tag = ImageFont.truetype(font_regular_file, size=25)
    font_text = ImageFont.truetype(font_regular_file, size=35)
    font_time_date = ImageFont.truetype(font_regular_file, size=24)
    font_reaction_regular = ImageFont.truetype(font_regular_file, size=30)
    font_reaction_bold = ImageFont.truetype(font_bold_file, size=30)
    font_quote_author_name = ImageFont.truetype(font_bold_file, size=27)
    font_quote_author_tag = ImageFont.truetype(font_regular_file, size=27)
    font_quote_text = ImageFont.truetype(font_regular_file, size=25)
    font_reply_author_name = ImageFont.truetype(font_bold_file, size=27)
    font_reply_author_tag = ImageFont.truetype(font_regular_file, size=27)
    font_reply_text = ImageFont.truetype(font_regular_file, size=25)

# global parameters
# positions
author_avatar_position = (35, 40)
author_name_position = (170, 40)
author_tag_position = (170, 95)
quote_author_avatar_position = (50, 40)
quote_author_name_position = (120, 45)
reply_author_avatar_position = (25, 30)
reply_author_name_position = (130, 30)
time_date_position = (35, 10)
reaction_retweet_position = (40, 80)  # Retweets
reaction_quote_position = (245, 80)  # Quote Tweets
reaction_like_position = (525, 80)  # Likes
text_position = (35, 0)
quote_text_position = (55, 0)
reply_text_position_y_adjust = -30
reply_text_position = (130, 0)
# measurements
header_height = 170
footer_height = 220
text_line_height = 45
quote_header_height = 100
quote_footer_height = 35
quote_text_line_height = 35
reply_header_height = 100
# reply_footer_height = 69
reply_text_line_height = 35
# backgrounds
header = Image.open('input/twitter_module/header.png').convert('RGB')
footer = Image.open('input/twitter_module/footer.png').convert('RGB')
quote_header = Image.open('input/twitter_module/quote_header.png').convert('RGB')
quote_background = Image.open('input/twitter_module/quote_background.png').convert('RGB')
quote_footer = Image.open('input/twitter_module/quote_footer.png').convert('RGB')
reply_header = Image.open('input/twitter_module/reply_header.png').convert('RGB')
# reply_footer = Image.open('input/twitter_module/reply_footer.png').convert('RGB')

# function to create tweet

def CreateTweet(
        author_avatar: str = "input/avatar/woman_clean.png",
        author_name: str = "User1",
        author_tag: str = "@user1",
        text: str = "Content of tweet.",
        reactions_retweet: str = "100",
        reactions_quote: str = "200",
        reactions_like: str = "20K",
        time: str = None,
        quote: bool = False,
        quote_author_avatar: str = "input/avatar/woman_clean.png",
        quote_author_name: str = "User2",
        quote_author_tag: str = "@user2",
        quote_text: str = "Content of quoted tweet.",
        reply: bool = False,
        reply_author_avatar: str = "input/avatar/woman_clean.png",
        reply_author_name: str = "User3",
        reply_author_tag: str = "@user3",
        reply_text: str = "Content of reply."
        ):
    """
    Create tweet using parameters.

    Parameters:
    author_avatar (str): avatar of author
    author_name (str): name of author
    author_tag (str): twitter username/handle of author
    text (str): main text of tweet
    reactions_retweet (str): number of reactions of tweet
    reactions_quote (str): number of quotes of tweet
    reactions_like (str): number of likes of tweet
    time (str/None): time of tweet in format "2022-07-05 14:34"; if None use current time
    quote (True/False): whether or not to print quoted tweet
    quote_author_avatar (str): avatar of author of quoted tweet
    quote_author_name (str): name of author of quoted tweet
    quote_author_tag (str): twitter username/handle of author of quoted tweet
    quote_text (str): text of quoted tweet
    reply (True/False): whether or not to print replied tweet
    reply_author_avatar (str): avatar of author of replied tweet
    reply_author_name (str): name of author of replied tweet
    reply_author_tag (str): twitter username/handle of author of replied tweet
    reply_text (str): text of replied tweet

    Returns:
    image: Twitter image in PIL format
    """

    # blank image to paste elements
    # calulate the number of lines for text and quote text
    text_string_lines = wrap(text, 54)
    quote_text_string_lines = wrap(quote_text, 77)
    reply_text_string_lines = wrap(reply_text, 70)
    height = header_height + footer_height + text_line_height * len(text_string_lines)
    if quote:
        height += quote_header_height + quote_footer_height + quote_text_line_height * len(quote_text_string_lines)
    if reply:
        height += reply_header_height + reply_text_line_height * len(reply_text_string_lines)
    img = Image.new(mode="RGB", size=(1050, height), color=(256, 256, 256))
    # header (include avatar and name), height=170
    img.paste(im=header, box=(0, 0))
    # author avatar
    author_avatar = Image.open(author_avatar).resize((100, 100))
    img.paste(im=author_avatar, box=author_avatar_position)
    # author name
    draw = ImageDraw.Draw(img)
    draw.text(xy=author_name_position, text=author_name,
              font=font_author_name, fill=(0, 0, 0))
    # author tag
    draw.text(xy=author_tag_position, text=author_tag,
              font=font_author_tag, fill="#667786")
    # text of main tweet
    # separate text into lists of each line and calculate y position for each line
    y = header_height
    for index, line in enumerate(text_string_lines):  # get the index and the text
        draw.text(
            xy=tuple(map(sum, zip(text_position, (0, y)))),
            text=line, font=font_text, fill=(0, 0, 0))
        y += text_line_height
    if quote:
        # quote header (include avatar and name), height=98
        img.paste(im=quote_header, box=(0, y))
        # quote author avatar
        quote_author_avatar = Image.open(quote_author_avatar).resize((50, 50))
        img.paste(
            im=quote_author_avatar,
            box=tuple(map(sum, zip(quote_author_avatar_position, (0, y)))))
        # quote author name
        draw.text(
            xy=tuple(map(sum, zip(quote_author_name_position, (0, y)))),
            text=quote_author_name, font=font_quote_author_name, fill=(0, 0, 0))
        # quote author tag
        quote_author_name_width = draw.textsize(
            text=quote_author_name,
            font=font_quote_author_name)[0]
        draw.text(
            xy=tuple(map(sum, zip(quote_author_name_position,
                     (10+quote_author_name_width, y)))),
            text=quote_author_tag, font=font_quote_author_tag, fill="#667786")
        # quote text
        # separate text into lists of each line and calculate y position for each line
        # get the index and the text
        y += quote_header_height
        for index, line in enumerate(quote_text_string_lines):
            img.paste(im=quote_background, box=(0, y-2))
            draw.text(
                xy=tuple(map(sum, zip(quote_text_position, (0, y)))),
                text=line, font=font_quote_text, fill=(0, 0, 0))
            y += quote_text_line_height
        img.paste(im=quote_footer, box=(0, y-2))
        y += quote_footer_height
    # footer (include reactions), height=260
    img.paste(im=footer, box=(0, y))
    # time
    if time is None:
        # get time from right now if no time given
        time = datetime.datetime.now()
        time.strftime("%Y-%m-%d %I:%M")
    else:
        # parse time according to "2022-07-05 14:34" format
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
    # format time to date and time in tweet format
    tweet_time = time.strftime("%-I:%M %p")
    tweet_date = time.strftime("%b %-d, %Y")
    time_date_text = tweet_time + " · " + tweet_date + " " + " "
    draw.text(xy=tuple(map(sum, zip(time_date_position, (0, y)))),
              text=time_date_text, font=font_time_date, fill="#667786")
    # reactions
    # retweets
    draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (0, y)))),
              text=reactions_retweet, font=font_reaction_bold, fill=(0, 0, 0))
    x_reactions = draw.textsize(text=reactions_retweet,
                                font=font_reaction_bold)[0] + 10
    draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (x_reactions, y)))),
              text="Reposts", font=font_reaction_regular, fill="#667786")
    x_reactions += draw.textsize(text="Reposts",
                                 font=font_reaction_regular)[0] + 30
    # quotes
    # remove quote tweets
    # draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (x_reactions, y)))),
    #          text=reactions_quote, font=font_reaction_bold, fill=(0, 0, 0))
    #x_reactions += draw.textsize(text=reactions_quote,
    #                             font=font_reaction_bold)[0] + 10
    #draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (x_reactions, y)))),
    #          text="Quote Tweets", font=font_reaction_regular, fill="#667786")
    #x_reactions += draw.textsize(text="Quote Tweets",
    #                             font=font_reaction_regular)[0] + 30
    # likes
    draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (x_reactions, y)))),
              text=reactions_like, font=font_reaction_bold, fill=(0, 0, 0))
    x_reactions += draw.textsize(text=reactions_like,
                                 font=font_reaction_bold)[0] + 10
    draw.text(xy=tuple(map(sum, zip(reaction_retweet_position, (x_reactions, y)))),
              text="Likes", font=font_reaction_regular, fill="#667786")
    x_reactions += draw.textsize(text="Likes",
                                 font=font_reaction_regular)[0] + 30
    if reply:
        y += footer_height
        # reply header (include avatar and name), height=126
        img.paste(im=reply_header, box=(0, y))
        # reply author avatar
        reply_author_avatar = Image.open(reply_author_avatar).resize((90, 90))
        img.paste(
            im=reply_author_avatar,
            box=tuple(map(sum, zip(reply_author_avatar_position, (0, y)))))
        # reply author name
        draw.text(
            xy=tuple(map(sum, zip(reply_author_name_position, (0, y)))),
            text=reply_author_name, font=font_reply_author_name, fill=(0, 0, 0))
        # reply author tag
        reply_author_name_width = draw.textsize(
            text=reply_author_name,
            font=font_reply_author_name)[0]
        draw.text(
            xy=tuple(map(sum, zip(reply_author_name_position,
                                  (10+reply_author_name_width, y)))),
            text=reply_author_tag, font=font_reply_author_tag, fill="#667786")
        # reply text
        # separate text into lists of each line and calculate y position for each line
        # get the index and the text
        y += reply_header_height
        y += reply_text_position_y_adjust
        for index, line in enumerate(reply_text_string_lines):
            draw.text(
                xy=tuple(map(sum, zip(reply_text_position, (0, y)))),
                text=line, font=font_reply_text, fill=(0, 0, 0))
            y += reply_text_line_height
        # img.paste(im=reply_footer, box=(0, y-2))
        # y += reply_footer_height
        

    return img
