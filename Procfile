user: hypercorn user --reload --debug --bind user.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
leaderboard: hypercorn leaderboard --reload --debug --bind leaderboard.local.gd:5101 --access-logfile - --error-logfile - --log-level DEBUG
primary: ./bin/litefs -config ./etc/primary.yml
secondary: ./bin/litefs -config ./etc/secondary.yml
tertiary: ./bin/litefs -config ./etc/tertiary.yml
