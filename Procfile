user: hypercorn user --reload --debug --bind user.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
leaderboard: hypercorn leaderboard --reload --debug --bind leaderboard.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG

game2: hypercorn game --reload --debug --bind game.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
game3: hypercorn game --reload --debug --bind game.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG

primary: bin/litefs -config ./etc/primary.yml
secondary: bin/litefs -config ./etc/secondary.yml
tertiary: bin/litefs -config ./etc/tertiary.yml
worker: rq worker --verbose --url redis://127.0.0.1:6379/3
