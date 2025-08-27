---
description: "Documentation and content creation standards"
applyTo: "hugo/content/**/*.md"
---

# Markdown Rules and Formatting Structure

Follow these rules for all markdown content:

## Front Matter

```toml
+++
date = 2024-02-02T04:14:54-08:00
draft = false
title = 'The title of the post.'
summary = 'A brief summary of the post.'
tags = ['tag1', 'tag2']
+++
```

- Include the following fields in the TOML front matter
- title and date are mandatory, other fields are optional.
- 160 chars for summary

## Headings

Use headings in a logical, hierarchical order:

- Use `##` for H2 and `###` for H3 headings. Avoid H4 or deeper unless absolutely necessary.
- Do not use H1; it will be generated automatically from the title.
- Format headings using attribute syntax, e.g.:

  `## Payment Methods {id="payment" class="h5 mt-5" icon="credit-card"}`

  - `id="payment"` (optional): sets the anchor ID; if not set, one will be generated.
  - `class="h5 mt-5"`: adds CSS classes. Use only Bootstrap classes or those from `hugo/assets/css/main.css`.
  - `icon="credit-card"`: adds a Bootstrap icon before the heading text.

- Hugo's custom heading renderer will automatically add icons, CSS classes, and anchor links.

## Lists

Use - for bullet points and 1. for numbered lists. Indent nested lists with two spaces. Ensure proper indentation and spacing.

## Links

- Internal links MUST use Hugo's ref or relref to avoid breakage when files move:
  - `[Support Team]({{< relref "company/contact/_index.md" >}})`
  - `[About Us]({{< ref "company/about/_index.md" >}})`
- Prefer `relref` for site‑internal navigation (relative to current page), `ref` when you want absolute canonical URL generation.
- External links use normal URLs: `[Microsoft Learn](https://learn.microsoft.com/)`
- For accessibility you can add a title attribute: `[Support Team]({{< relref "company/contact/_index.md" >}} "Contact our support team")`
- Do not hard‑code `/company/.../` paths; use ref/relref to prevent broken links.

## Images

![alt text](images/product/widget.jpg)

- ("alt text"); recommend instructing meaningful descriptive text for images.

## Tables

```markdown
| Name   | Warranty | Price  |
| ------ | -------- | ------ |
| Widget | 1 year   | $10.00 |
| Gizmo  | 2 years  | $15.00 |

{ border="true" }
```

- Use default table styling for most tables; add `{ border="true" }` only when a visible border is needed.
- The attribute block must be placed immediately after the table, with no blank line in between.

## Code Blocks

- Use triple backticks (```) for fenced code blocks. Specify the language after the opening backticks for syntax highlighting (e.g., csharp).
- Use backticks for inline code with short identifiers.

## Line Length

Limit lines to 100-120 characters for readability.

## Whitespace

- Use blank lines to separate sections and improve readability. Avoid excessive whitespace.
- Single blank line before headings and after lists
- Trimming trailing spaces.
