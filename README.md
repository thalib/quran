# quran

## Prompts 

### Proofread

```
Proofread the selected text for spelling and grammar errors. Additionally, identify and remove any redundant sentences or phrases, and rephrase for clarity and conciseness.
```

## shortcodes

### quran

```
{{< quran v="chapter:verse" trans="translation" >}}
```

```
<!-- Single verse -->
{{< quran v="1:1" >}}

<!-- Single verse with specific translation -->
{{< quran v="1:1" trans="sahih" >}}

<!-- Range of verses -->
{{< quran v="2:1-3" >}}

<!-- Range with specific translation -->
{{< quran v="2:255-257" trans="sahih" >}}
```

### qurantt - tool tip

```
{{< qurantt v="chapter:verse" trans="translation" >}}
```

```
<!-- Single verse -->
{{< qurantt v="1:1" >}}

<!-- Single verse with specific translation -->
{{< qurantt v="1:1" trans="sahih" >}}

<!-- Range of verses -->
{{< qurantt v="2:1-3" >}}

<!-- Range with specific translation -->
{{< qurantt v="2:255-257" trans="sahih" >}}
```

### quranhl - highlight

```
{{< quranhl v="chapter:verse" trans="translation" hl="start-end" >}}
```

```
<!-- Simple verse without highlighting -->
{{< quranhl v="1:1" >}}

<!-- Verse with specific translation -->
{{< quranhl v="1:1" trans="sahih" >}}

<!-- Verse with highlighting -->
{{< quranhl v="2:255" hl="1-20" >}}

<!-- Verse with translation and highlighting -->
{{< quranhl v="2:255" trans="sahih" hl="15-35" >}}
```

### arabic 

```
{{< arabic color="light" title="Chapter Title" >}}
Arabic text content here
{{< /arabic >}}
```

```
<!-- Basic Arabic text with dark theme -->
{{< arabic >}}
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
{{< /arabic >}}

<!-- Arabic text with light theme -->
{{< arabic color="light" >}}
الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
{{< /arabic >}}

<!-- Arabic text with title and light theme -->
{{< arabic color="light" title="Al-Fatiha" >}}
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
{{< /arabic >}}

<!-- Arabic text with title but dark theme -->
{{< arabic title="Verse 1" >}}
وَالْعَصْرِ
{{< /arabic >}}
```

### wfw

```
{{< wfw eng="word1,word2,word3" >}}
كلمة١
كلمة٢
كلمة٣
{{< /wfw >}}
```


```
<!-- Basic word-for-word translation -->
{{< wfw eng="In,the,name,of,Allah,the,Beneficent,the,Merciful" >}}
بِسْمِ
اللَّهِ
الرَّحْمَٰنِ
الرَّحِيمِ
{{< /wfw >}}

<!-- Shorter phrase -->
{{< wfw eng="Praise,be,to,Allah" >}}
الْحَمْدُ
لِلَّهِ
{{< /wfw >}}

<!-- With longer phrases -->
{{< wfw eng="And,when,they,meet,those,who,believe" >}}
وَإِذَا
لَقُوا
الَّذِينَ
آمَنُوا
{{< /wfw >}}
```