# --- Replace or insert this block where OpenAI key is read / AI is called ---

import os
import traceback

def _get_sanitized_api_key():
    """
    Returns (api_key_or_None, note_or_None)
    - Tries st.secrets, then ENV.
    - Strips whitespace, surrounding quotes, BOM.
    - If non-ascii chars exist, attempts to remove them and returns note.
    """
    raw = None
    note = None

    # 1) try st.secrets first (Streamlit Cloud)
    try:
        raw = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        raw = None

    # 2) fallback to environment variable (local)
    if not raw:
        raw = os.environ.get("OPENAI_API_KEY")

    if not raw:
        return None, "NO_KEY"

    orig_repr = repr(raw)

    # strip whitespace, newline
    api = raw.strip()

    # if user accidentally stored with quotes included, remove
    if api.startswith('"') and api.endswith('"'):
        api = api[1:-1]

    # remove common BOM
    if api.startswith("\ufeff"):
        api = api.lstrip("\ufeff")

    # If there are non-ascii characters, create an ascii-only sanitized version
    non_ascii = [ch for ch in api if ord(ch) >= 128]
    if non_ascii:
        # Attempt to remove non-ascii chars (this is a last-resort; ideally user corrects secret)
        api_ascii = "".join(ch for ch in api if ord(ch) < 128)
        note = f"NON_ASCII_REMOVED (orig_repr={orig_repr})"
        # If sanitized looks like a plausible key (starts with sk-), return it.
        if api_ascii.startswith("sk-"):
            return api_ascii, note
        # else return sanitized anyway but signal user
        return api_ascii, note

    # otherwise OK
    return api, None


def _test_and_call_openai(api_key, prompt, max_results=3):
    """
    Try-call OpenAI using installed library.
    This app assumes old 0.28 API (ChatCompletion.create) but will try to use it defensively.
    Returns (success(bool), result_or_error_text)
    """
    try:
        import openai
    except Exception as e:
        return False, f"openai lib import failed: {e}"

    # set api key
    try:
        openai.api_key = api_key
    except Exception as e:
        # This usually shouldn't fail, but catch
        return False, f"Failed to assign api_key: {e}"

    # Call ChatCompletion.create (0.28 style). Wrap in try.
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            max_tokens=400
        )
        # try multiple ways to extract text
        try:
            content = response.choices[0].message["content"]
        except Exception:
            try:
                content = response.choices[0].message.content
            except Exception:
                content = str(response)
        return True, content
    except Exception as e:
        # capture full traceback to show to user (shortened)
        tb = traceback.format_exc()
        return False, f"OpenAI call failed: {e}\n{tb}"


# Example use inside your main flow:
# 1) build prompt as before, e.g.:
# prompt = f"... 키워드: {', '.join(keywords)}"

api_key, note = _get_sanitized_api_key()

# show debug info (collapsible) so user can see what's stored (repr)
with st.expander("🔧 OpenAI Key debug (확인 후 숨기세요)"):
    st.write("raw st.secrets or ENV repr:", repr(st.secrets.get("OPENAI_API_KEY") if st.secrets else None))
    st.write("sanitized key repr:", repr(api_key))
    st.write("note:", note)

if not api_key:
    # no key -> skip AI and fallback to local
    st.info("OPENAI API 키가 설정되어 있지 않거나 형식 오류가 있습니다. 자체 추천으로 대체합니다.")
    # call your local_recommend(...) here
else:
    # sanity check: key should start with sk-
    if not api_key.startswith("sk-"):
        st.warning("OPENAI_API_KEY가 'sk-'로 시작하지 않습니다. 올바른 키인지 확인해주세요. 자체 추천으로 대체됩니다.")
        # fallback to local
    else:
        # try AI call
        # build prompt as you did
        success, out = _test_and_call_openai(api_key, prompt)
        if success:
            # display AI output
            st.subheader("🎵 AI 추천 결과 (OpenAI)")
            st.markdown(out)
        else:
            # show clear error to user and fallback
            st.error("AI 호출 실패 — 자체 추천으로 대체합니다.")
            with st.expander("AI 실패 상세 (개발용)"):
                st.write(out)
            # fallback to local_recommend(...)
