---
name: "multi-search-engine"
description: "Search and cross-check public web information across 16 Chinese and international engines without API keys. Use for multi-engine research, current information checks, site/filetype/time-filtered searches, privacy-oriented search, and WolframAlpha queries; triggers include multi search, web research, 多引擎搜索, 全网搜索, 限定站点搜索, and 时效检索."
---

# Multi Search Engine

Integration of 16 search engines for web research without API keys.

## Workflow

1. **Preparation**: Identify which search and browsing capabilities are actually available in the current runtime. Prefer the runtime's built-in web search/browser tools first; only fall back to raw HTTP or shell-based fetching when those capabilities are explicitly available.

2. **Language Evaluation**: Detect the language attribute of the search query. If the query is in Chinese, use Domestic search engines (Baidu, Bing CN, Bing INT, 360, Sogou, WeChat, Shenma). If the query is non-Chinese, use International search engines (Google, Google HK, DuckDuckGo, Yahoo, Startpage, Brave, Ecosia, Qwant, WolframAlpha). Select engines based on query relevance and availability.

3. **Controlled Search**: Execute search requests with the current runtime's available web tools:
   - Prefer first-party search/browser tools when present
   - Add 1-2 second delay between requests to respect server load
   - Batch requests in groups of 3-4 engines with sequential execution between batches
   - If a runtime supports custom headers or browser sessions, use them conservatively
   - If access is denied (403/429), switch engines or reduce request volume before attempting any session refresh

4. **Session Management**:
   - Only use cookies/session state if the current runtime actually exposes browser or HTTP session controls
   - Keep any session state ONLY in memory during runtime
   - Do not read from or write to config files just to persist cookies
   - Clear transient session state after the search session completes
   - If the runtime does not expose cookie/session controls, skip this step and rely on engine switching or built-in search tools

5. **Retry Mechanism**: If a search fails due to session, throttling, or access issues, retry once after a short delay or switch to another engine. Do not loop indefinitely.

6. **Result Aggregation**: Consolidate successful results from search engines, organize and summarize them to output a core search report

**CHECKPOINT:** If the query is ambiguous enough to change the subject, jurisdiction, or time range, ask one focused clarification before searching. If it contains private personal data, credentials, or a request to bypass access controls, stop and narrow the request to lawful public information.

## Failure Recovery

| Trigger | First response | If it still fails |
|---|---|---|
| One engine returns 403/429 or CAPTCHA | Switch to a different engine and reduce request frequency | Exclude the blocked engine and report the coverage gap |
| A runtime has no web capability | Request network/browser access only when live results are required | Provide query URLs and search operators without claiming they were executed |
| Results disagree | Compare source date, primary-source status, and independent corroboration | Present the disagreement explicitly; do not force a single conclusion |
| Results are stale | Add a time filter and search the official domain directly | State the newest verified date and label the answer incomplete |
| No credible result is found | Broaden one term or use one synonym, then retry once | Stop and report “not verified”; do not fill gaps from memory |

## Output Format

Return results in this order:

1. **Answer:** concise conclusion limited to verified findings.
2. **Evidence:** source title, publisher/domain, publication date when available, and direct link.
3. **Cross-check:** which independent engines or primary sources corroborate the claim.
4. **Gaps:** blocked engines, stale evidence, disagreements, and facts not verified.
5. **Queries used:** include the final search expressions only when they help reproducibility.

## Search Engines

### Domestic (7)
- **Baidu**: `https://www.baidu.com/s?wd={keyword}`
- **Bing CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **Bing INT**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **Sogou**: `https://sogou.com/web?query={keyword}`
- **WeChat**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **Shenma**: `https://m.sm.cn/s?q={keyword}`

### International (9)
- **Google**: `https://www.google.com/search?q={keyword}`
- **Google HK**: `https://www.google.com.hk/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Yahoo**: `https://search.yahoo.com/search?p={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`

## Quick Examples

```text
Basic search:
https://www.google.com/search?q=python+tutorial

Site-specific:
https://www.google.com/search?q=site:github.com+react

File type:
https://www.google.com/search?q=machine+learning+filetype:pdf

Time filter (past week):
https://www.google.com/search?q=ai+news&tbs=qdr:w

Privacy search:
https://duckduckgo.com/html/?q=privacy+tools

DuckDuckGo Bangs:
https://duckduckgo.com/html/?q=!gh+tensorflow

Knowledge calculation:
https://www.wolframalpha.com/input?i=100+USD+to+CNY
```

## Advanced Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Search within site |
| `filetype:` | `filetype:pdf report` | Specific file type |
| `""` | `"machine learning"` | Exact match |
| `-` | `python -snake` | Exclude term |
| `OR` | `cat OR dog` | Either term |

## Time Filters

| Parameter | Description |
|-----------|-------------|
| `tbs=qdr:h` | Past hour |
| `tbs=qdr:d` | Past day |
| `tbs=qdr:w` | Past week |
| `tbs=qdr:m` | Past month |
| `tbs=qdr:y` | Past year |

## Privacy Engines

- **DuckDuckGo**: No tracking
- **Startpage**: Google results + privacy
- **Brave**: Independent index
- **Qwant**: EU GDPR compliant

## Bangs Shortcuts (DuckDuckGo)

| Bang | Destination |
|------|-------------|
| `!g` | Google |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | Wikipedia |
| `!yt` | YouTube |

## WolframAlpha Queries

- Math: `integrate x^2 dx`
- Conversion: `100 USD to CNY`
- Stocks: `AAPL stock`
- Weather: `weather in Beijing`

## Documentation

- `references/advanced-search.md` - Domestic search guide
- `references/international-search.md` - International search guide
- `CHANGELOG.md` - Version history

## License

MIT

## Security & Privacy Notice

### Session Handling
- **Purpose**: Session state may be used ONLY when the current runtime supports it and access failures make it necessary
- **Storage**: Any transient session state should remain in memory only
- **Acquisition**: Acquire session state on-demand only if the runtime exposes browser/HTTP session controls
- **Fallback**: If session control is unavailable, switch engines, reduce request rate, or use built-in search tools instead
- **Lifecycle**: Clear transient session state after the search session completes
- **No Pre-configuration**: Do not load cookies from config files or external files at startup
- **No API Keys**: This skill is designed around public search URLs and runtime-native web tools

### Crawling Ethics
- **Rate Limiting**: Implement reasonable delays between requests (recommend 1-2 seconds)
- **Respect robots.txt**: Honor search engine crawling policies
- **Terms of Service**: Users are responsible for complying with search engine ToS
- **Purpose**: Designed for legitimate search aggregation, not mass data scraping

### Data Handling
- **No Personal Data**: Tool should not intentionally collect or persist user personal information
- **Runtime-dependent Transport**: Requests may be executed by built-in web tools or available shell/browser capabilities in the current runtime
- **Session Isolation**: Any transient session state should be session-specific and cleared after use

## Do Not Do These

- Do not claim that an engine was searched when only a query URL was constructed.
- Do not treat search-result snippets as authoritative evidence when the underlying page is available.
- Do not bypass CAPTCHAs, access controls, robots rules, or rate limits.
- Do not persist cookies, credentials, personal data, or search histories in the skill directory.
- Do not combine conflicting results into a confident conclusion without showing the disagreement.
