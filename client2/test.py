import redis
import time

r = redis.Redis(host = 'localhost', port = '6379')

def upper():
    next_value = 0
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                pipe.watch('counter')
                current_value = int(pipe.get('counter')) if pipe.get('counter') else 0
                next_value = current_value + 1
                pipe.multi()
                pipe.set('counter', next_value, None)
                print("value:",  next_value)
                pipe.execute()
                
                break
            except redis.WatchError:
                # show which counter is used by another user
                print("revoked:", next_value)
                error_count += 1

for item in range(10):
    time.sleep(0.5)
    upper()
