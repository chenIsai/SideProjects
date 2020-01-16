"""Author: Isaiah Chen

   Date: May 31 2017

   Description: This program contains the mainline logic for the Plants vs Zombie game, utilizing sprites from the pvzSprites.py module. This program also multiple functions: game(), instructions(), spawn_wave() and high_score()
"""
#Import and Initialize
import pygame, pvzSprites
pygame.init()
pygame.mixer.init()

def game(screen):
    """This function represents the main game which in the Plants vs Zombies game. This function takes the screen as a parameter, and will return True/False depending on whether a full game was played, and the score of the game, with 0 being returned if the game was not completed"""
    #Entities
    background = pygame.image.load("./Images/background.png")
    background.convert()
    screen.blit(background, (0, 0))
    #Sound Effects/Music
    shot = pygame.mixer.Sound("./Audio/projectile.wav")
    lose_life = pygame.mixer.Sound("./Audio/loseLife.wav")
    house_collide = pygame.mixer.Sound("./Audio/houseLoseLife.wav")
    death = pygame.mixer.Sound("./Audio/death.wav")
    shot.set_volume(0.5)
    lose_life.set_volume(0.7)
    house_collide.set_volume(0.7)
    death.set_volume(0.5)
    pygame.mixer.music.load("./Audio/background.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    #Sprites for:
    scorekeeper = pvzSprites.Scorekeeper()
    house = pvzSprites.House(0, 0)
    player = pvzSprites.Player(screen)
    endzone = pvzSprites.EndZone(screen)
    upgrade = pvzSprites.Upgrade()
    #Groups of Sprites
    projectileGroup = pygame.sprite.Group()
    zombieGroup = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(house, upgrade, scorekeeper, player)
    #Action - Broken down into ALTER

    #Assign Variables
    clock = pygame.time.Clock()
    keepGoing = True
    cooldown = False
    tempTime = 0
    in_progress = False
    cooldown_time = .5
    bul_health = 1
    damage = 3
    upgrade_list = [[0, 4, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1]]
    funds = 0
    upgrading = False
    spawning = True

    #Loop
    while keepGoing:
        #Time
        clock.tick(30)
        #Spawn in a new wave
        if not in_progress:
            total = (scorekeeper.get_waves()+4) * (scorekeeper.get_waves()+1)
            zombies = spawn_wave(total, scorekeeper.get_waves())
            zombieGroup.add(zombies)
            wave_total = len(zombies)
            allSprites.add(zombies)
            in_progress = not in_progress
            spawning = False
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        #Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            player.go_down()
        elif keys[pygame.K_UP]:
            player.go_up()
        elif keys[pygame.K_RIGHT]:
            player.go_right()
        elif keys[pygame.K_LEFT]:
            player.go_left()
        #Fires a round if the space key is pressed/held
        if keys[pygame.K_SPACE] and not cooldown:
            projectile = pvzSprites.Projectile(player.rect.right, player.rect.top, 5, damage, bul_health)
            projectileGroup.add(projectile)
            allSprites.add(projectile)
            player.firing()
            shot.play()
            cooldown = not cooldown
            tempTime = scorekeeper.get_time()
        #Changes player fire cooldown based on scorekeeper time
        if scorekeeper.get_time() - cooldown_time >= tempTime:
            cooldown = not cooldown
        #Check if wave is over
        if not zombieGroup and not upgrading and not spawning:
            scorekeeper.win_wave()
            scorekeeper.add_funds(wave_total*2)
            funds += wave_total*2
            player.increase_speed()
            upgrading = True
        if not zombieGroup and spawning:
            in_progress = not in_progress
        #Upgrade section after every wave is won
        if upgrading:
            player.reset()
            upgrade.show_image()
            #Options from 1 through to 4
            if keys[pygame.K_1]:
                if funds - upgrade_list[0][1] >= 0:
                    funds -= upgrade_list[0][1]
                    scorekeeper.add_funds(-upgrade_list[0][1])
                    upgrade_list[0][1] = upgrade_list[0][1] + 4
                    cooldown_time /= 1.4
            elif keys[pygame.K_2]:
                if funds - upgrade_list[1][1] >= 0:
                    funds -= upgrade_list[1][1]
                    scorekeeper.add_funds(-upgrade_list[1][1])
                    upgrade_list[1][1] = upgrade_list[1][1] + 4
                    damage += 1
            elif keys[pygame.K_3]:
                if funds - upgrade_list[2][1] >= 0:
                    funds -= upgrade_list[2][1]
                    scorekeeper.add_funds(-upgrade_list[2][1])
                    upgrade_list[2][1] = upgrade_list[2][1] + 4
                    scorekeeper.add_lives()
            elif keys[pygame.K_4]:
                if funds - upgrade_list[3][1] >= 0:
                    funds -= upgrade_list[3][1]
                    scorekeeper.add_funds(-upgrade_list[3][1])
                    upgrade_list[3][1] = upgrade_list[3][1] + 4
                    bul_health += 1
            elif keys[pygame.K_b]:
                upgrading = False
                upgrade.hide_image()
                spawning = True

        #Zombie and Projectile Collision Detection
        for projectile in projectileGroup:
            zombieHit = pygame.sprite.spritecollide(projectile, zombieGroup, False)
            if zombieHit:
                for zombie in zombieHit:
                    hitList = projectile.get_zomhits()
                    if zombie not in hitList:
                        projectile.add_zomhits(zombie)
                        zombie.lose_health(projectile.get_damage())
                        projectile.hit()
                    if projectile.get_health() <= 0:
                        projectile.kill()
                        projectileGroup.remove(projectile)
                    if zombie.get_health() <= 0:
                        zombie.kill()
                        zombieGroup.remove(zombie)
                        scorekeeper.killed_zombie()
                        death.play()
                        scorekeeper.player_scored(zombie.get_points())
        #Kills projectiles if they reach the end of the screen
        for projectile in projectileGroup:
            if projectile.rect.colliderect(endzone):
                projectile.kill()
                projectileGroup.remove(projectile)
        #Collision Detection for Zombie and Player
        zomPlayHit = pygame.sprite.spritecollide(player, zombieGroup, False)
        if zomPlayHit:
            for zombie in zomPlayHit:
                zombie.kill()
                zombieGroup.remove(zombie)
                scorekeeper.player_scored(-10)
                player.reset()
            shot.play()
            scorekeeper.lose_life()
        #Collision Detection for House and PLayer
        houseHit = pygame.sprite.spritecollide(house, zombieGroup, False)
        if houseHit:
            for zombie in houseHit:
                zombie.kill()
                zombieGroup.remove(zombie)
                scorekeeper.player_scored(-10)
            scorekeeper.lose_life()
            house_collide.play()
        #Check if Player has run out of Lives
        if scorekeeper.get_lives() <= 0:
            return True, scorekeeper.get_score()

        scorekeeper.set_time(float(pygame.time.get_ticks())/1000)


        #Refresh Display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

    return False, 0

def spawn_wave(totalZombies, waves):
    """This function is a helper function for the game() function. It takes 2 parameters, which is the total number of zombies wanted, and the total number of waves the player has completed. This function returns a list of zombie sprites."""
    zombies = []
    x = 980
    #For loop to generate zombies
    for zombie in range(totalZombies):
        zombies.append(pvzSprites.Zombie(x, waves))
        x += 10
    return zombies

def instructions(screen):
    """This function displays the instructions which are shown before the main game takes place. This function takes the screen as a parameter, and returns True/False depending on whether the user wishes to continue playing or not"""
    #Has its own game loop
    #Entities
    background = pygame.image.load("./Images/introduction.png")
    screen.blit(background, (0, 0))
    #Assign Variables
    clock = pygame.time.Clock()
    keepGoing = True

    #Loop
    while keepGoing:
        #Time
        clock.tick(30)
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    return True
                #Refresh Display
            pygame.display.flip()
    return False

def main():
    """This function represents the mainline logic of the Plants vs Zombies Program. It calls 3 functions: Instructions, game, and high_score"""
    pygame.init()
    #Display
    screen = pygame.display.set_mode((960, 480))
    pygame.display.set_caption("Plants Vs Zombies")

    status = instructions(screen)
    if status:
        pygame.time.wait(1000)
        status, score = game(screen)
    if status:
        high_score(score, screen)
    pygame.quit()


def high_score(score, screen):

    #Import and Initialize
    high_scorefile = open("highscores.txt", "a")
    #Entities
    background = pygame.image.load("./Images/highscore.png")
    screen.blit(background, (0, 0))
    #Assign Values
    name = " "
    highscoreFont = pygame.font.Font("gang.ttf", 20)
    text = highscoreFont.render(name, 1, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (440, 250)
    message = name
    clock = pygame.time.Clock()
    keepGoing = True
    #Loop
    while keepGoing:
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                    screen.blit(background, (0, 0))
                elif event.key == pygame.K_RETURN:
                    message = [name, score]
                    high_scorefile.write(str(message))
                    keepGoing = False
        #Refresh Display
        message = name
        text = highscoreFont.render(name, 1, (0, 0, 0))
        screen.blit(text, textRect)
        pygame.display.flip()
    high_scorefile.close()

main()
