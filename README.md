<table style="border: 1px solid transparent">
  <tr>
    <td>
<a href="http://talky.readthedocs.io"><img src="https://img.shields.io/badge/Wiki-%23000000.svg?style=for-the-badge&logo=wikipedia&logoColor=white"></a>
<a href="https://github.com/mraniki/tt/"><img src="https://img.shields.io/badge/github-%23000000.svg?style=for-the-badge&logo=github&logoColor=white"></a><br>
<a href="https://hub.docker.com/r/mraniki/tt"><img src="https://img.shields.io/docker/pulls/mraniki/tt?style=for-the-badge"></a><br>
       </td>
    <td align="center"><img width="200" alt="Logo" src="/docs/_static/logo-full.png"></td>
  </tr>
  <tr>
    <td>
      <a href="https://pypi.org/project/myllm/"><img src="https://img.shields.io/pypi/v/myllm?style=for-the-badge&logo=PyPI&logoColor=white"></a><br>
      <a href="https://pypi.org/project/myllm/"><img src="https://img.shields.io/pypi/dm/myllm?style=for-the-badge&logo=PyPI&logoColor=white"></a><br>
      <a href="https://github.com/mraniki/myllm/"><img src="https://img.shields.io/github/actions/workflow/status/mraniki/myllm/%F0%9F%91%B7Flow.yml?style=for-the-badge&logo=GitHub&logoColor=white"></a><br>
      <a href="https://talky.readthedocs.io/projects/myllm/"><img src="https://readthedocs.org/projects/myllm/badge/?version=latest&style=for-the-badge"></a><br>
      <a href="https://codebeat.co/projects/github-com-mraniki-myllm-main"><img src="https://codebeat.co/badges/0567b9d9-3cbb-4263-80ec-8ac8043332ea"/></a> <br>
      <a href="https://app.codacy.com/gh/mraniki/MyLLM/dashboard"><img src="https://app.codacy.com/project/badge/Grade/75f2650d58044355957fe667aeed50a1"/></a> <br>
      <a href="https://codecov.io/gh/mraniki/myllm"><img src="https://codecov.io/gh/mraniki/myllm/branch/main/graph/badge.svg?token=WAHUEMAJN6"/></a><br>
    </td>
    <td align="left"> 
Interact with LLM in simple way,<br>via  <a href="https://github.com/xtekky/gpt4free">G4F</a>, <a href="https://github.com/openai/openai-python">OPENAI</a>/<a href="https://localai.io/basics/getting_started/">LOCALAI</a><br>
  </td>   
  </tr>
</table>


<h5>How to use it</h5>
<pre>
<code>
    talky = MyLLM()

    chat = await talky.chat("My name is Jack")
    print(chat)
    # 🐻 Hello Jack, this is Bing. I'm happy to help you with general tasks. 😊

    chat = await talky.chat("tell me who is president of the united states?")
    print(chat)
    # The current president of the United States is **Joe Biden**[^1^][1] [^2^][2].
    # He took office on **January 20, 2021**[^1^][1] [^2^][2].
    # He is the **46th** president of the United States[^2^][2] [^3^][5].

    chat = await talky.chat("what is my name")
    print(chat)
    # 🐻 You told me your name is Jack. Is that correct?

    await talky.export_chat_history()
    # talky.clear_chat_history()
</code>
</pre>

<h5>Documentation</h5>
<a href="https://talky.readthedocs.io/projects/myllm/en/latest/"><img src="https://img.shields.io/badge/Documentation-000000?style=for-the-badge&logo=readthedocs&logoColor=white"></a><br>
