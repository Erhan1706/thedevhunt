<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="static/assets/favicon.ico" alt="Logo" width="40" height="40">
  </a>

<h3 align="center">TheDevHunt</h3>

  <p align="center">
    <a href="https://thedevhunt.com/"><strong>https://thedevhunt.com/</strong></a>
    <br />
    A network of web scrapers that collect tech job postings daily, from the most prominent companies in Europe, all aggregated into a single website.
    <br />
    <br />
    <!--
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    --> 
  </p>

</div>

<!-- TABLE OF CONTENTS
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
-->

<!-- ABOUT THE PROJECT -->

## About The Project

[![TheDevHunt Screen Shot][product-screenshot]](https://thedevhunt.com)

TheDevHunt is a comprehensive job aggregation platform designed for tech professionals seeking opportunities across Europe. By utilizing a network of web scrapers, we collect and curate job postings from the most prominent tech companies daily, ensuring that our users have access to the latest and most relevant openings in the industry. Whether you're a developer, IT specialist, or data scientist, TheDevHunt is your gateway to finding your next big career move.

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.
<!--
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- npm
  ```sh
  npm install npm@latest -g
  ```
-->
### Installation

Note: Some libraries used in this project may have compatibility issues on Windows.

1. Clone the repo
   ```sh
   git clone https://github.com/Erhan1706/thedevhunt.git
   ```
2. Create a local .env file and with the following ke-value pairs:
  ```
  DJANGO_DEBUG=True
  DJANGO_PRODUCTION=False
  DJANGO_SECRET_KEY=<YOU SECRET KEY>

  ### POSTGRES CONFIGS
  POSTGRES_USER=<YOUR USERNAME>
  POSTGRES_PASSWORD=<YOUR PASSWORD>
  POSTGRES_HOST=<YOUR HOST>
  POSTGRES_PORT=<YOUR PORT>
  POSTGRES_DB=<YOUR DB NAME>
  ```
3. Start the development server:
   ```sh
   docker compose up --build
   ```
4. **If you make any changes to the frontend styling, make sure to compile the tailwind in a separate terminal**, otherwise you won't see the differences:
   ```sh
   ./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
   ```

<!-- USAGE EXAMPLES
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->

<!-- See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues). -->

<!-- CONTRIBUTING -->

## Contributing

Any contributions made are **greatly appreciated**.

A logical contribution would be adding a scraper for a different company not yet supported. The listings are fetched from the backend api of the companies, usually I avoid scraping the main page directly and parsing the html. All the scrapers are at `api/scrapers`, they essentially follow the same template. The main challenge is the fact that each company has their data in different formats, so in same cases custom functionality needs to be included per scraper. The most common functions to be implemented for each scraper are: `filter_eu_jobs`, `filter_tech_jobs`, `scrape`, and `transform_data` which maps how the json is translated to the Job schema, to be stored in the db.  


If you have a suggestion that would make this better, please fork the repo and create a pull request.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some amazing feature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<br>
<br>
<br>

<!-- LICENSE
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->

<!-- CONTACT -->

Contact at: dorian.erhan@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: static/assets/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
