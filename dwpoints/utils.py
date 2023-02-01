#
# HELPERS
#
def log(msg,noisy,level='INFO'):
    if noisy:
        print(f"[{level}] DW_POINTS: {msg}")