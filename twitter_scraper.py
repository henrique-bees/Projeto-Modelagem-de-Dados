from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

def scrape_twitter_selenium_v2(username, max_tweets=500):
    """Coleta tweets usando Selenium com scroll otimizado"""
    
    chrome_options = Options()
    # Remover headless para ver o que está acontecendo
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    tweets_data = []
    seen_tweets = set()
    
    try:
        url = f'https://twitter.com/{username}'
        print(f"Acessando {url}...")
        driver.get(url)
        
        print("Aguardando carregamento da página...")
        time.sleep(5)
        
        last_count = 0
        no_new_tweets_count = 0
        
        while len(tweets_data) < max_tweets:
            # Encontrar todos os tweets na página
            try:
                articles = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                print(f"Encontrados {len(articles)} elementos article na página")
                
                for article in articles:
                    try:
                        # Tentar pegar o texto do tweet
                        tweet_text_elem = article.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                        tweet_text = tweet_text_elem.text
                        
                        # Evitar duplicatas
                        if tweet_text in seen_tweets or not tweet_text:
                            continue
                        
                        seen_tweets.add(tweet_text)
                        
                        # Tentar pegar a data
                        try:
                            time_elem = article.find_element(By.TAG_NAME, 'time')
                            tweet_date = time_elem.get_attribute('datetime')
                        except:
                            tweet_date = ''
                        
                        # Tentar pegar métricas
                        try:
                            metrics = article.find_elements(By.CSS_SELECTOR, '[role="group"] span')
                            replies = metrics[0].text if len(metrics) > 0 else '0'
                            retweets = metrics[1].text if len(metrics) > 1 else '0'
                            likes = metrics[2].text if len(metrics) > 2 else '0'
                        except:
                            replies = retweets = likes = '0'
                        
                        # Tentar pegar URL do tweet
                        try:
                            link = article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                            tweet_url = link.get_attribute('href')
                        except:
                            tweet_url = ''
                        
                        tweets_data.append({
                            'autor': username,
                            'descricao': tweet_text,
                            'data': tweet_date,
                            'likes': likes,
                            'retweets': retweets,
                            'respostas': replies,
                            'url': tweet_url
                        })
                        
                        if len(tweets_data) >= max_tweets:
                            break
                    
                    except Exception as e:
                        continue
                
                print(f"Total coletado: {len(tweets_data)} tweets únicos")
                
                # Verificar se não está coletando mais tweets
                if len(tweets_data) == last_count:
                    no_new_tweets_count += 1
                    if no_new_tweets_count >= 5:
                        print("Não há mais tweets novos. Finalizando...")
                        break
                else:
                    no_new_tweets_count = 0
                    last_count = len(tweets_data)
                
                if len(tweets_data) >= max_tweets:
                    break
                
                # Scroll para baixo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
            except Exception as e:
                print(f"Erro ao processar tweets: {e}")
                time.sleep(2)
    
    finally:
        print("Fechando navegador...")
        driver.quit()
    
    return tweets_data

if __name__ == "__main__":
    USERNAME = "Apple"
    MAX_TWEETS = 500
    
    print(f"Iniciando coleta de tweets de @{USERNAME}...")
    tweets = scrape_twitter_selenium_v2(USERNAME, MAX_TWEETS)
    
    if tweets:
        df = pd.DataFrame(tweets)
        filename = f"tweets_{USERNAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✓ {len(tweets)} tweets salvos em '{filename}'")
        print(f"\nPrimeiros tweets coletados:")
        print(df[['autor', 'descricao']].head(10))
    else:
        print("\n✗ Nenhum tweet foi coletado.")
