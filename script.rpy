init python:

    def roomEvents(event, x, y, at):
        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            for item in roomSprites:
                if item.x <= x <= (item.x + item.width) and item.y <= y <= (item.y + item.height):
                    t = Transform(child = item.hover_image)
                    item.set_child(t)
                    roomSpriteManager.redraw(0)
                else:
                    t = Transform(child = item.idle_image)
                    item.set_child(t)
                    roomSpriteManager.redraw(0)
        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            for item in roomSprites:
                if item.x <= x <= (item.x + item.width) and item.y <= y <= (item.y + item.height):
                    if item.type in possibleInventoryItems:
                        addToInventory(item.type)
                    elif item.type == "bookshelf" and bookshelfPuzzleComplete == False:
                        renpy.show_screen("bookshelf")
                        renpy.restart_interaction()
                    elif item.type == "summoningpanel":
                        renpy.show_screen("summoningpanel")
                        renpy.restart_interaction()

    def inventoryUpdate(st):
        if inventoryDrag == True:
            for itemPlace, item in enumerate(inventorySprites):
                if itemPlace == itemNumberDragged:
                    item.x = mousePosition[0] - item.width/2
                    item.y = mousePosition[1] - item.height/2
                    item.zorder = 99
            return 0
        return None

    def inventoryEvents(event, x, y, at):
        global mousePosition
        global inventoryDrag
        global itemOverlap
        global itemNumberDragged 
        global moonplant
        global piranhaplant
        global waterplant
        global firstingredient
        global secondingredient
        global thirdingredient
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONDOWN:
            for itemPlace, item in enumerate(inventorySprites):
                if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                    itemNumberDragged = itemPlace
                    startDrag(item)
        elif event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousePosition = (x, y)
        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            for item in inventorySprites:
                if item.type == itemDragged:
                    inventoryDrag = False
                    for item2 in roomSprites:
                        if item2.x <= x <= item2.x + item2.width and item2.y <= y <= item2.y + item2.height:
                            if item.type == "paper" and item2.type == "book":
                                removeInventorySprite(item)
                            if item.type == "shears" and item2.type == "overgrownplant":
                                removeInventorySprite(item)
                                removeRoomSprite(item2)
                            if item.type == "plantpotion" and item2.type == "moonplantpot":
                                moonplant = True
                                removeInventorySprite(item)
                                renpy.jump("gardenWall")
                            if item.type == "plantpotion" and item2.type == "piranhaplantpot":
                                piranhaplant = True
                                removeInventorySprite(item)
                                renpy.jump("gardenWall")
                            if item.type == "plantpotion" and item2.type == "waterplantpot":
                                waterplant = True
                                removeInventorySprite(item)
                                renpy.jump("gardenWall")
                            if item.type == "plantpotion" and item2.type == "rainbowplantpot":
                                removeInventorySprite(item)
                                removeRoomSprite(item2)
                                addToInventory("thirdingredient")
                                renpy.show_screen("inventory")
                            if item.type == "firstingredient" and item2.type == "potionstand":
                                firstingredient = True
                                removeInventorySprite(item)
                                checkWin()
                                renpy.jump("potionWall")
                            if item.type == "secondingredient" and item2.type == "potionstand":
                                secondingredient = True
                                removeInventorySprite(item)
                                checkWin()
                                renpy.jump("potionWall")
                            if item.type == "thirdingredient" and item2.type == "potionstand":
                                thirdingredient = True
                                removeInventorySprite(item)
                                checkWin()
                                renpy.jump("potionWall")
                            
            if itemOverlap == False:
                for item in inventorySprites:
                    if item.type == itemDragged:
                        item.x = item.original_x
                        item.y = item.original_y

    def changeWall(arrowClicked):
        global wallNumber
        if arrowClicked == "left":
            if wallNumber > 0: 
                wallNumber -= 1
            else:
                wallNumber = 3

        if arrowClicked == "right":
            if wallNumber < 3:
                wallNumber += 1
            else:
                wallNumber = 0

        renpy.jump(walls[wallNumber])

    def addToInventory(item):
        
        inventory.append(item)

        item_image = Image("inventory/{}_inventory.png".format(item))

        t = Transform(child = item_image)

        inventorySprites.append(inventorySpriteManager.create(t))
        
        inventorySprites[-1].height = 145
        inventorySprites[-1].width = 145
        inventorySprites[-1].type = item
        inventorySprites[-1].item_image = item_image
        inventorySprites[-1].y = 800
        inventorySprites[-1].original_y = 800 

        repositionInventoryItems()

        for currentSprite in roomSprites:
            if currentSprite.type == item:
                removeRoomSprite(item = currentSprite)
                break

        inventorySpriteManager.redraw(0)
        roomSpriteManager.redraw(0)
        renpy.restart_interaction()

    def repositionInventoryItems():
        for item in range(0, len(inventory)):
            inventorySprites[item].x = 435 + (item*180)
            inventorySprites[item].original_x = inventorySprites[item].x
            inventorySprites[item].y = 800

    def removeRoomSprite(item):
        item.destroy()
        roomSprites.pop(roomSprites.index(item))
        roomItems.pop(roomItems.index(item.type))
        roomItemsDeleted.append(item.type)

    def removeInventorySprite(item):
        item.destroy()
        inventorySprites.pop(inventorySprites.index(item))
        inventory.pop(inventory.index(item.type))
        repositionInventoryItems()

    def startDrag(item):
        global inventoryDrag
        global itemDragged
        inventoryDrag = True
        itemDragged = item.type
        inventorySpriteManager.redraw(0)

    def bookCode(book):
        global secretCode 
        global bookshelfPuzzleComplete
        if book == "book1" and secretCode == 0:
            secretCode += 1
        elif book == "book2" and secretCode == 1:
            secretCode += 1    
        elif book == "book3" and secretCode == 2:
            secretCode += 1    
        elif book == "book4" and secretCode == 3:
            secretCode += 1    
        else:
            secretCode = 0

        if secretCode == 4:
            bookshelfPuzzleComplete = True
            renpy.hide_screen("bookshelf")
            renpy.restart_interaction()
            addToInventory("shears")
            addToInventory("firstingredient")
            renpy.show_screen("inventory")
            renpy.jump("libraryWall")          

    def togglePanel(panel):
        global secondingredientsleft
        global plantpotionsleft
        
        if panels[panel] == "UI/panel_%s.png":
            panels[panel] = "UI/panelclicked_%s.png"
        else:
            panels[panel] = "UI/panel_%s.png"

        plantpotion = True
        secondingredient = True
        for x in range(0, len(panels)):
            if panels[x] != secondingredientpanels[x]:
                secondingredient = False
            if panels[x] != plantpotionpanels[x]:
                plantpotion = False
        
        if secondingredient == True and secondingredientsleft > 0:
            secondingredientsleft -= 1
            addToInventory("secondingredient")
            resetPanel()

        if plantpotion == True and plantpotionsleft > 0:
            plantpotionsleft -= 1
            addToInventory("plantpotion")
            resetPanel()

    def resetPanel():
        renpy.hide_screen("summoningpanel")
        renpy.restart_interaction()
        renpy.show_screen("inventory")
        for x in range(0, len(panels)):
            panels[x] = "UI/panel_%s.png"

    def checkWin():
        if firstingredient == True and secondingredient == True and thirdingredient == True:
            renpy.show_screen("win")
        
screen ui:
    modal True

    add roomSpriteManager

    zorder 1

    imagebutton auto "UI/leftarrow_%s.png" xpos 64 ypos 817 focus_mask True action Function(changeWall, "left")

    imagebutton auto "UI/rightarrow_%s.png" xpos 1720 ypos 817 focus_mask True action Function(changeWall, "right")

    imagebutton auto "UI/inventorybutton_%s.png" xpos 24 ypos 17 focus_mask True action If(renpy.get_screen("inventory") == None, true = Show("inventory"), false = Hide("inventory"))

screen inventory:

    zorder 1

    image "UI/inventory_bar.png" xpos 405 ypos 790

    add inventorySpriteManager

screen book:
    
    zorder 2

    image "UI/book.png" xpos 235 ypos 134

    imagebutton auto "UI/exitbutton_%s.png" xpos 1562 ypos 631 focus_mask True action Hide("book")


screen bookshelf:

    modal True

    zorder 2

    image "UI/bookshelf.png" xpos 265 ypos 88

    imagebutton auto "UI/bookRed_%s.png" xpos 357 ypos 251 focus_mask True action Function(bookCode, "book1")
    imagebutton auto "UI/bookOrange_%s.png" xpos 432 ypos 251 focus_mask True action Function(bookCode, "book2")
    imagebutton auto "UI/bookGreen_%s.png" xpos 509 ypos 230 focus_mask True action Function(bookCode, "book3")
    imagebutton auto "UI/bookPurple_%s.png" xpos 609 ypos 230 focus_mask True action Function(bookCode, "book4")
    imagebutton auto "UI/bookYellow_%s.png" xpos 719 ypos 251 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookBlue_%s.png" xpos 796 ypos 251 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookGreenRight_%s.png" xpos 1264 ypos 220 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookPurpleRight_%s.png" xpos 1363 ypos 220 focus_mask True action Function(bookCode, "book3")
    imagebutton auto "UI/bookBlue_%s.png" xpos 362 ypos 652 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookGreenLeft_%s.png" xpos 391 ypos 565 focus_mask True action Function(bookCode, "book4")
    imagebutton auto "UI/bookRed_%s.png" xpos 786 ypos 652 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookPurple_%s.png" xpos 873 ypos 635 focus_mask True action Function(bookCode, "other book")
    imagebutton auto "UI/bookYellow_%s.png" xpos 984 ypos 652 focus_mask True action Function(bookCode, "book2")
    imagebutton auto "UI/bookOrange_%s.png" xpos 1060 ypos 652 focus_mask True action Function(bookCode, "other book")

    imagebutton auto "UI/exitbutton_%s.png" xpos 1575 ypos 97 focus_mask True action Hide("bookshelf")

screen summoningpanel:
    
    modal True

    zorder 2

    image "UI/summoningpanel.png" xpos 495 ypos 75

    imagebutton auto panels[0] xpos 566 ypos 150 focus_mask True action Function(togglePanel, 0)
    imagebutton auto panels[1] xpos 828 ypos 150 focus_mask True action Function(togglePanel, 1)
    imagebutton auto panels[2] xpos 1090 ypos 150 focus_mask True action Function(togglePanel, 2)
    imagebutton auto panels[3] xpos 566 ypos 406 focus_mask True action Function(togglePanel, 3)
    imagebutton auto panels[4] xpos 828 ypos 406 focus_mask True action Function(togglePanel, 4)
    imagebutton auto panels[5] xpos 1090 ypos 406 focus_mask True action Function(togglePanel, 5)
    imagebutton auto panels[6] xpos 566 ypos 665 focus_mask True action Function(togglePanel, 6)
    imagebutton auto panels[7] xpos 828 ypos 665 focus_mask True action Function(togglePanel, 7)
    imagebutton auto panels[8] xpos 1090 ypos 665 focus_mask True action Function(togglePanel, 8)

    imagebutton auto "UI/exitbutton_%s.png" xpos 1359 ypos 82 focus_mask True action Hide("summoningpanel")
    
screen win:

    modal True

    zorder 2

    image "UI/winimage.png" xpos 0 ypos 0

    imagebutton auto "UI/retry_%s.png" xpos 407 ypos 736 focus_mask True action MainMenu()

    imagebutton auto "UI/quit_%s.png" xpos 1167 ypos 736 focus_mask True action Quit()

label start:

    $roomSpriteManager = SpriteManager(event=roomEvents)
    $inventorySpriteManager = SpriteManager(update = inventoryUpdate, event = inventoryEvents)

    $roomSprites = []
    $roomItems = []

    $walls = ["potionWall", "gardenWall", "libraryWall", "summonerWall"]
    $wallNumber = 0

    $inventorySprites = []
    $inventory = []
    $possibleInventoryItems = ["paper"]

    $inventoryDrag = False
    $itemDragged = ""
    $mousePosition = (0.0, 0.0)
    $itemOverlap = False
    $itemNumberDragged = 0

    $roomItemsDeleted = []
    
    $secretCode = 0
    $bookshelfPuzzleComplete = False

    $panels = ["UI/panel_%s.png", "UI/panel_%s.png", "UI/panel_%s.png", 
            "UI/panel_%s.png", "UI/panel_%s.png", "UI/panel_%s.png", 
            "UI/panel_%s.png", "UI/panel_%s.png", "UI/panel_%s.png"]

    $secondingredientpanels = ["UI/panelclicked_%s.png", "UI/panel_%s.png", "UI/panel_%s.png", 
            "UI/panel_%s.png", "UI/panelclicked_%s.png", "UI/panelclicked_%s.png", 
            "UI/panelclicked_%s.png", "UI/panelclicked_%s.png", "UI/panel_%s.png"]

    $plantpotionpanels = ["UI/panelclicked_%s.png", "UI/panelclicked_%s.png", "UI/panel_%s.png", 
            "UI/panelclicked_%s.png", "UI/panel_%s.png", "UI/panel_%s.png", 
            "UI/panelclicked_%s.png", "UI/panel_%s.png", "UI/panelclicked_%s.png"]

    $secondingredientsleft = 1
    $plantpotionsleft = 4

    $moonplant = False
    $piranhaplant = False
    $waterplant = False

    $firstingredient = False
    $secondingredient = False
    $thirdingredient = False

    hide screen win

    show screen ui
    
    jump potionWall

label main:
    
    pause 

    return 

label potionWall:
    scene potionwallbg

    $roomItems = ["potionstand", "book"]

    if firstingredient == True:
        $roomItems.append("firstingredient")

    if secondingredient == True:
        $roomItems.append("secondingredient")

    if thirdingredient == True:
        $roomItems.append("thirdingredient")

    python:
        for item in roomSprites:
            item.destroy()
            roomSpriteManager.redraw()
        roomSprites = []

        for item in roomItems:
            if item not in roomItemsDeleted:
                idle_image = Image("potionwall/{}_idle.png".format(item))
                hover_image = Image("potionwall/{}_hover.png".format(item))

                t = Transform(child = idle_image)
                sprite = roomSpriteManager.create(t)
                roomSprites.append(sprite)

                roomSprites[-1].type = item
                roomSprites[-1].idle_image = idle_image
                roomSprites[-1].hover_image = hover_image
                
                if item == "potionstand":
                    roomSprites[-1].width = 333
                    roomSprites[-1].height = 284
                    roomSprites[-1].x = 793
                    roomSprites[-1].y = 330

                if item == "book":
                    roomSprites[-1].width = 321
                    roomSprites[-1].height = 168
                    roomSprites[-1].x = 1537
                    roomSprites[-1].y = 463

                if item == "firstingredient":
                    roomSprites[-1].width = 45
                    roomSprites[-1].height = 72
                    roomSprites[-1].x = 799
                    roomSprites[-1].y = 478

                if item == "secondingredient":
                    roomSprites[-1].width = 36
                    roomSprites[-1].height = 34
                    roomSprites[-1].x = 860
                    roomSprites[-1].y = 515
                    
                if item == "thirdingredient":
                    roomSprites[-1].width = 42
                    roomSprites[-1].height = 75
                    roomSprites[-1].x = 917
                    roomSprites[-1].y = 476

    jump main

label gardenWall:
    scene gardenwallbg

    $roomItems = ["moonplantpot", "piranhaplantpot", "waterplantpot", "rainbowplantpot", "overgrownplant"]

    if moonplant == True:
        $roomItems[0] = "moonplant"

    if piranhaplant == True:
        $roomItems[1] = "piranhaplant"

    if waterplant == True:
        $roomItems[2] = "waterplant"

    python:
        for item in roomSprites:
            item.destroy()
            roomSpriteManager.redraw(0)
        roomSprites = []

        for item in roomItems:
            if item not in roomItemsDeleted:
                idle_image = Image("gardenwall/{}_idle.png".format(item))
                hover_image = Image("gardenwall/{}_hover.png".format(item))

                t = Transform(child = idle_image)
                sprite = roomSpriteManager.create(t)
                roomSprites.append(sprite)

                roomSprites[-1].type = item
                roomSprites[-1].idle_image = idle_image
                roomSprites[-1].hover_image = hover_image

                if item == "moonplantpot":
                    roomSprites[-1].width = 124
                    roomSprites[-1].height = 112
                    roomSprites[-1].x = 234
                    roomSprites[-1].y = 680

                if item == "piranhaplantpot":
                    roomSprites[-1].width = 124
                    roomSprites[-1].height = 112
                    roomSprites[-1].x = 553
                    roomSprites[-1].y = 380

                if item == "waterplantpot":
                    roomSprites[-1].width = 124
                    roomSprites[-1].height = 112
                    roomSprites[-1].x = 249
                    roomSprites[-1].y = 380

                if item == "rainbowplantpot":
                    roomSprites[-1].width = 124
                    roomSprites[-1].height = 112
                    roomSprites[-1].x = 553
                    roomSprites[-1].y = 680

                if item == "overgrownplant":
                    roomSprites[-1].width = 787
                    roomSprites[-1].height = 1102
                    roomSprites[-1].x = 1068
                    roomSprites[-1].y = -126

                if item == "moonplant":
                    roomSprites[-1].width = 166
                    roomSprites[-1].height = 230
                    roomSprites[-1].x = 206
                    roomSprites[-1].y = 562

                if item == "piranhaplant":
                    roomSprites[-1].width = 141
                    roomSprites[-1].height = 235
                    roomSprites[-1].x = 553
                    roomSprites[-1].y = 256

                if item == "waterplant":
                    roomSprites[-1].width = 234
                    roomSprites[-1].height = 283
                    roomSprites[-1].x = 194
                    roomSprites[-1].y = 208

    jump main

label libraryWall:
    if bookshelfPuzzleComplete == False:
        $roomItems = ["paper", "bookshelf", "chest"]
    else: 
        $roomItems = ["paper", "bookshelf", "open chest"]
    python:
        for item in roomSprites:
            item.destroy()
            roomSpriteManager.redraw(0)
        roomSprites = []

        for item in roomItems:
            if item not in roomItemsDeleted:
                idle_image = Image("librarywall/{}_idle.png".format(item))
                hover_image = Image("librarywall/{}_hover.png".format(item))

                t = Transform(child = idle_image)
                sprite = roomSpriteManager.create(t)
                roomSprites.append(sprite)

                roomSprites[-1].type = item
                roomSprites[-1].idle_image = idle_image
                roomSprites[-1].hover_image = hover_image

                if item == "paper":
                    roomSprites[-1].width = 230
                    roomSprites[-1].height = 201
                    roomSprites[-1].x = 982
                    roomSprites[-1].y = 772

                if item == "bookshelf":
                    roomSprites[-1].width = 698
                    roomSprites[-1].height = 850
                    roomSprites[-1].x = 629
                    roomSprites[-1].y = 41

                if item == "chest":
                    roomSprites[-1].width = 375
                    roomSprites[-1].height = 335
                    roomSprites[-1].x = 121
                    roomSprites[-1].y = 673

                if item == "open chest":
                    roomSprites[-1].width = 376
                    roomSprites[-1].height = 393
                    roomSprites[-1].x = 120
                    roomSprites[-1].y = 616

                if item == "shears":
                    roomSprites[-1].width = 152
                    roomSprites[-1].height = 88
                    roomSprites[-1].x = 267
                    roomSprites[-1].y = 693

                if item == "first ingredient":
                    roomSprites[-1].width = 121
                    roomSprites[-1].height = 69
                    roomSprites[-1].x = 135
                    roomSprites[-1].y = 736
    jump main

label summonerWall:
    scene summonerwallbg
    
    $roomItems = ["summoningpanel"]

    python:
        for item in roomSprites:
            item.destroy()
            roomSpriteManager.redraw(0)
        roomSprites = []

        for item in roomItems:
            if item not in roomItemsDeleted:
                idle_image = Image("summonerwall/{}_idle.png".format(item))
                hover_image = Image("summonerwall/{}_hover.png".format(item))

                t = Transform(child = idle_image)
                sprite = roomSpriteManager.create(t)
                roomSprites.append(sprite)

                roomSprites[-1].type = item
                roomSprites[-1].idle_image = idle_image
                roomSprites[-1].hover_image = hover_image

                if item == "summoningpanel":
                    roomSprites[-1].width = 291
                    roomSprites[-1].height = 416
                    roomSprites[-1].x = 1417
                    roomSprites[-1].y = 582

    jump main




