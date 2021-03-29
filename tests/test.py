import sys
sys.path.append("../src/")

import twitcasting


def main() -> None:
    user = "izayoikaede"
    video_id = twitcasting.get_video_id(user)
    is_live = twitcasting.is_user_live(user)
    fmp4_sock_address = twitcasting.get_fmp4_sock_address(user)
    llfmp4_sock_address = twitcasting.get_llfmp4_sock_address(user)
    is_clippable = twitcasting.is_stream_clippable(video_id)
    live_title = twitcasting.get_live_title(user)
    token = twitcasting.generate_token(video_id=video_id)
    live_status = twitcasting.get_live_viewer_status(token, video_id)

    print("VideoId", video_id)
    print("isLive?", is_live)
    print("fmp4SockAddr", fmp4_sock_address)
    print("llfmp4SockAddr", llfmp4_sock_address)
    print("isClippable?", is_clippable)
    print("liveTitle", live_title)
    print("token", token)
    print("liveStatus", live_status)


if __name__ == "__main__":
    main()

