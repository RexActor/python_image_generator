from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from enum import Enum
import textwrap
import time
# Change


class RARITY(Enum):
    Junk = "Junk"
    Poor = "Poor"
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    UNIQUE = "Unique"


class COLORTYPE(Enum):
    BACKGROUND = "Background"
    FONT = "Font"


def DrawLine(startPos, endPos, distanceFromTop, targetImage, color):
    drawLine = ImageDraw.Draw(targetImage)
    lineShape = [(startPos, distanceFromTop), (endPos, distanceFromTop)]
    drawLine.line(lineShape, fill=(color), width=2)
    return drawLine


def GetRarityColor(_rarity, option):
    rarityColor = None
    rarityFontColor = None
    if _rarity is RARITY.Junk:
        rarityColor = (44, 44, 46, 0)
        rarityFontColor = (44, 44, 46, 255)
    elif _rarity is RARITY.Poor:
        rarityColor = (138, 135, 131, 25)
        rarityFontColor = (138, 135, 131, 255)
    elif _rarity is RARITY.COMMON:
        rarityColor = (117, 115, 113, 40)
        rarityFontColor = (117, 115, 113, 255)
    elif _rarity is RARITY.UNCOMMON:
        rarityColor = (58, 176, 21, 40)
        rarityFontColor = (58, 176, 21, 255)
    elif _rarity is RARITY.RARE:
        rarityColor = (32, 129, 227, 40)
        rarityFontColor = (32, 129, 227, 255)
    elif _rarity is RARITY.EPIC:
        rarityColor = (100, 13, 133, 40)
        rarityFontColor = (100, 13, 133, 255)
    elif _rarity is RARITY.LEGENDARY:
        rarityColor = (214, 142, 9, 40)
        rarityFontColor = (214, 142, 9, 255)
    elif _rarity is RARITY.UNIQUE:
        rarityColor = (190, 191, 130, 50)
        rarityFontColor = (190, 191, 130, 255)

    if option is COLORTYPE.FONT:
        return rarityFontColor
    elif option is COLORTYPE.BACKGROUND:
        return rarityColor


def GenerateImage(_rarity, _ItemName, _itemImageFileName, _itemDamage, _moveSpeed, _requiredClass, _slotType, _handType, _weaponType, _attackSpeed, _flavourText, _modifierList=None):

    offsetIncrease = 30  # offset to move objects lower if modifiers are being displayed
    # region size for Image

    width = 322  # 322
    _moveItemOffset = 0
    if _modifierList is not None:
        _moveItemOffset = len(_modifierList)*40

    height = 770 + _moveItemOffset
# endregionf


# region ASSIGN FONTS

    HeaderFont = ImageFont.truetype('oswald/Oswald-Medium.ttf', 30)
    _weaponDamageFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 20)
    _moveSpeedFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 20)
    _modifierFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 16)
    ItemDetailMainFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 18)
    flavourTextFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 20)
    _requiredClassFont = ImageFont.truetype('oswald/Oswald-Light.ttf', 20)

# endregion


# region ASSIGN COLORS

    MainItemNameColor = (238, 238, 238, 255)
    rarityColor = GetRarityColor(_rarity, COLORTYPE.BACKGROUND)
    rarityFontColor = GetRarityColor(_rarity, COLORTYPE.FONT)
    blackColor = (0, 0, 0, 255)
    defaultTextColor50Transparent = (255, 255, 255, 50)
    orangeTextColor = (255, 172, 28, 255)
    whiteTextColor = (255, 255, 255, 255)
    flavourTextColor = (105, 69, 19, 255)
    modifierColor = rarityColor

# endregion

# region CREATE REQUIRED IMAGES AND FIELDS
    backgroundImage = Image.new(mode="RGB", size=(
        width, height), color=(blackColor))  # background image created
    # Front page image where is "Rarity colours displayed" is created with Alpha mode
    frontImage = Image.new(mode="RGBA", size=(width, 80), color=(rarityColor))
    # Adds frontImage on top of background image
    backgroundImage.paste(frontImage, mask=frontImage)

    ItemImage = Image.open(f'{_itemImageFileName}',
                           mode='r')  # Opens Item image
    w, h = ItemImage.size
    Resized_ItemImage = ItemImage.resize(
        (w, h))  # Resizes new imported Image
    # border around picture (if required increase float)
    newIMg = ImageOps.expand(Resized_ItemImage, (0, 0, 0, 0), fill=rarityColor)
    backgroundImage.paste(
        newIMg, (((width-w)//2), (height-h)//7), mask=newIMg)  # Pastes Image on top of Background

# endregion


# region CREATE TOP BOX FOR ITEM NAME

    # creates shape size - [(start_position),(end_position)]

    lineShape = [(0, 0), (width-1, 80)]

    drawboxLine = ImageDraw.Draw(backgroundImage)  # creates instance?
    drawboxLine.rectangle((lineShape),
                          width=2, outline=rarityFontColor)  # actually draws rectangle with rarity font color (due that Rarity font color don't have transparency enabled)

    ItemNameText = ImageDraw.Draw(backgroundImage)
    ItemNameText.text((width//4, 20), _ItemName,
                      font=HeaderFont, fill=(rarityFontColor))  # Creates Item name and displays it

# endregion

# region DRAWS WAPON DAMAGE AND MOVE SPEED REGION

    DrawLine(30, width - 30, 320, backgroundImage,
             MainItemNameColor)  # draw line after Item image

    DrawLine(20, 30, 360, backgroundImage,
             MainItemNameColor)  # Draws (-) before Damage text

    WeaponDamage = ImageDraw.Draw(backgroundImage)
    w = WeaponDamage.textlength(_itemDamage)
    WeaponDamage.text(
        (((width-w)/2)-20, 350), f"{_itemDamage}", font=_weaponDamageFont, fill=(defaultTextColor50Transparent))

    DrawLine(width-40, width-30, 360, backgroundImage,
             MainItemNameColor)  # Draws(-) after Damage text

    # Draws(-) before Move Speed text
    DrawLine(20, 30, 400, backgroundImage, MainItemNameColor)

    MoveSpeed = ImageDraw.Draw(backgroundImage)
    w = MoveSpeed.textlength(_moveSpeed)
    MoveSpeed.text(
        (((width-w)/2)-20, 390), f"{_moveSpeed}", font=_moveSpeedFont, fill=(defaultTextColor50Transparent))

    DrawLine(width-40, width-30, 400, backgroundImage,
             MainItemNameColor)  # Draws(-) after Move Speed text
# endregion

# region GENERATE MODIFIERS IF REQUIRED
    if _modifierList is not None:
        modifierOffset = 0  # Offset which one is increasing by 40 after each iteration
        for item in _modifierList:

            DrawLine(20, 30, 440+modifierOffset,
                     backgroundImage, modifierColor)

            modifier = ImageDraw.Draw(backgroundImage)
            w = modifier.textlength(item[0])

            modifier.text(((width-w)/2, 430+modifierOffset),
                          f"{item[0]}", font=_modifierFont, fill=(modifierColor))

            DrawLine(width-40, width-30, 440+modifierOffset,
                     backgroundImage, modifierColor)

            modifierOffset = modifierOffset+40

# endregion


# region CREATE ITEM DETAIL REGION

    # region REQUIRED CLASS
    # Draw Required Class text

    RequiredClassMain = ImageDraw.Draw(backgroundImage)
    RequiredClass = ImageDraw.Draw(backgroundImage)
    w = RequiredClass.textlength(_requiredClass)
    RequiredClassMain.text(
        ((width-w)/2, 450+_moveItemOffset), f"Required Class:", font=ItemDetailMainFont, fill=(defaultTextColor50Transparent))

    RequiredClass.text(
        ((width-w)/2, 475+_moveItemOffset), f"{_requiredClass}", font=_requiredClassFont, fill=(orangeTextColor))
    # endregion

    # region SLOT TYPE
    # Draw SlotType Text

    SlotTypeMain = ImageDraw.Draw(backgroundImage)

    SlotType = ImageDraw.Draw(backgroundImage)
    w = SlotType.textlength(_slotType)
    SlotTypeMain .text(
        (((width-w)/2)-32, 510+_moveItemOffset), f"Slot Type:", font=ItemDetailMainFont, fill=(defaultTextColor50Transparent))

    SlotType.text(
        (((width-w)/2)+32, 510+_moveItemOffset), f"{_slotType}", font=ItemDetailMainFont, fill=whiteTextColor)
    # endregion

    # region HAND TYPE
    # DRAW hand Type
    HandTypeMain = ImageDraw.Draw(backgroundImage)

    HandType = ImageDraw.Draw(backgroundImage)
    w = HandType.textlength(_handType)
    HandTypeMain .text(
        (((width-w)/2)-35, 535+_moveItemOffset), f"Hand Type:", font=ItemDetailMainFont, fill=(defaultTextColor50Transparent))

    HandType = ImageDraw.Draw(backgroundImage)
    HandType.text(
        (((width-w)/2)+35, 535+_moveItemOffset), f"{_handType}", font=ItemDetailMainFont, fill=whiteTextColor)
    # endregion

    # region Weapon Type
    # DRAW Weapon Type
    WeaponTypeMain = ImageDraw.Draw(backgroundImage)
    WeaponType = ImageDraw.Draw(backgroundImage)
    w = WeaponType.textlength(_weaponType)
    WeaponTypeMain .text(
        (((width-w)/2)-45, 560+_moveItemOffset), f"Weapon Type:", font=ItemDetailMainFont, fill=(defaultTextColor50Transparent))

    WeaponType.text(
        (((width-w)/2)+45, 560+_moveItemOffset), f"{_weaponType}", font=ItemDetailMainFont, fill=(orangeTextColor))

    DrawLine(30, width - 30, 630+_moveItemOffset,
             backgroundImage, MainItemNameColor)
    # endregion

# endregion

# region FLAVOUR TEXT
    # draw flavour text

    margin = offset = 40

    for line in textwrap.wrap(_flavourText, width=40):
        flavourText = ImageDraw.Draw(backgroundImage)
        flavourText.text((30, 610+offset+_moveItemOffset), line,
                         font=flavourTextFont, fill=(flavourTextColor))
        offset += offsetIncrease
# endregion

    # ACTUALLY SAVES THE FILE WITH 95 Quality (highest)
    backgroundImage.save('test.png', quality=95)


for rarity in RARITY:

    GenerateImage(rarity, "Arming Sword", "neckles.png", "Damage 40", "Move Speed -100",
                  "Fighter, Cleric", "Primary Weapon",
                  "Double-Handed", "Sword",
                  "0.6s/0.56s/0.75s",
                  "If you are reading This . Then It means that I finished Image generator script! Was fun! and not that hard!",
                  [["Up to 5 extra enchantments"], [
                      "+15 additional Dark Magical Damage"], ["Up to 4 extra enchantments"]]

                  )
    time.sleep(1)
