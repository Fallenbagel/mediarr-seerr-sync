#!/bin/bash
arr_sync_ip=http://192.168.100.153:5000
if [ "$radarr_eventtype" = "MovieDelete" ]; then
	/usr/bin/curl -X POST -H "Content-Type: application/json" -d "{\"title\": \"$radarr_movie_title\", \"tmdb_id\": $radarr_movie_tmdbid}" $arr_sync_ip/webhook
elif [ "$sonarr_eventtype" = "SeriesDelete" ]; then
	/usr/bin/curl -X POST -H "Content-Type: application/json" -d "{\"title\": \"$sonarr_series_title\", \"imdb_id\": \"$sonarr_series_imdbid\", \"tvdb_id\": $sonarr_series_tvdbid}" $arr_sync_ip/webhook
fi
