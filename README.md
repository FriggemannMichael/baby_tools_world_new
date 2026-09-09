# Baby Tools World

Baby Tools World is a Django shop demo for browsing baby products, exploring categories and sharing ratings and reviews. Administrators manage the catalog and assign reusable product tags through Django Admin. The application is an educational project; checkout and payment are not implemented.

## Table of Contents

- [Quickstart](#quickstart)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
- [Development](#development)
- [Running with Docker](#running-with-docker)
- [Documentation](#documentation)
- [License](#license)

## Quickstart

### Prerequisites

- Python 3.12, as specified in `.python-version`.
- Git for cloning the repository.
- Docker only when using the [container workflow](#running-with-docker).

1. Clone the repository: `git clone https://github.com/FriggemannMichael/baby_tools_world_new.git`.
1. Enter the repository: `cd baby_tools_world_new`.
1. Create a virtual environment: `python -m venv .venv`.
1. Activate it: `.\.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux.
1. Install dependencies: `python -m pip install -r requirements.txt`.
1. Copy the configuration: `cp example.env src/.env` (PowerShell: `Copy-Item example.env src/.env`).
1. Enter `src` with `cd src`, then apply the migrations: `python manage.py migrate`.
1. Add sample products: `python manage.py seed_db`.
1. Create an admin account: `python manage.py createsuperuser` and follow the prompts.
1. Start the server: `python manage.py runserver`. Open <http://localhost:8000/> or sign in at <http://localhost:8000/admin/>.

### Alternative: using uv

If you use [uv](https://docs.astral.sh/uv/), replace the virtual environment and dependency steps with these commands from the repository root:

```shell
uv venv
uv pip install -r requirements.txt
```

Activate `.venv` as described above and continue with the configuration step. You can also run management commands through `uv run python manage.py ...` from `src` without activating the environment manually.

## Features

- **Product catalog and categories:** Browse the home page or select a category to narrow the product list. Open a product to see its price, description and image, with placeholders for missing descriptions or images.
- **Product tags:** Create tags such as `Limited` in Django Admin and assign one or more to a product. Product details display all assigned tags or the italic text `no tags available` when none are selected.
- **User accounts:** Register, log in and log out through the website. Regular registered accounts do not automatically have access to Django Admin.
- **Ratings and reviews:** Submit one to five stars and an optional comment, either signed in or as a guest providing a name and email. Signed-in users update their previous review when submitting again; the form clears after successful submission.
- **Related products:** Product details show up to eight other products from the same category, ordered by average rating, rating count and name. Use a product's Details link to open it.
- **Administration:** Manage products, categories, tags and reviews through Django Admin. Filter products by tag or search tags by name.
- **Sample data:** Run `seed_db` to create four categories and 15 sample products with bundled images. Existing entries with the same names are skipped; tags are added separately in Django Admin.

## Repository Structure

The project files are organized as follows:

- `.github/`: Contains GitHub Actions workflows and pull request templates.
- `.gitlab/` and `.gitlab-ci.yml`: Contain the GitLab templates and pipeline configuration.
- `docs/`: Contains testing and WSGI guides, the original submission checklist and verification notes.
- `src/btw_app/`: Defines Django settings, application URLs and server entry points.
- `src/products/`: Contains the catalog, tags, reviews, admin configuration, migrations, tests and seed command.
- `src/users/`: Handles registration, login and logout.
- `src/templates/`: Contains shared page templates.
- `src/static/`: Contains static assets and bundled product images.
- `src/manage.py`: Provides Django management commands.
- `Dockerfile` and `entrypoint.sh`: Build and start the application container.
- `example.env`: Documents the application environment variables.
- `requirements.txt` and `pyproject.toml`: Define pinned dependencies and Python linting configuration.
- `README.md` and `LICENSE`: Provide project documentation and licensing information.

The SQLite database, uploaded images and collected static files are generated locally and ignored by Git.

## Usage

### Browsing products

Open <http://localhost:8000/>, choose a category and select **See Details** on a product. The detail page displays its tags, customer reviews and related products. If the catalog is empty, follow [Sample data](#sample-data) or create products in Django Admin.

The **Buy now** element is a visual placeholder.

### Accounts and reviews

Register at <http://localhost:8000/users/register/>, then sign in at <http://localhost:8000/users/login/>. On a product detail page, choose a star rating, optionally enter a comment and select **Submit Review**. Guests also enter their name and email address.

A successful submission updates the reviews and rating summary and clears the form. When signed in, submitting again for the same product updates your existing review. Use the website's logout link to end your session.

### Managing products and tags

1. Open <http://localhost:8000/admin/> and sign in with the superuser account created during Quickstart.
1. Open **Categories** and add a category with a name and unique slug. Under **Products**, add a product with a name, category and price; description, image and tags are optional.
1. Open **Tags**, select **Add tag**, enter a unique name such as `Limited` and save. Creation and update timestamps are managed automatically and cannot be edited.
1. Edit a product such as `baby-bottle`. Move `Limited` from the available tags to the chosen tags and save.
1. Open the product's detail page and check the **Product-Tags** section. Assign several tags to display them together, or remove all tags to display the italic `no tags available` placeholder.

Tags can be reused across products. Use the tag filter in the admin product list to find matching products and **Comments** to manage submitted reviews.

To create another admin account, run `python manage.py createsuperuser` from `src` in a terminal with the virtual environment activated.

### Configuration

Copy `example.env` to `src/.env` before starting the application. The file contains these settings:

| Variable | Purpose | Default |
| --- | --- | --- |
| `ALLOWED_HOSTS` | Comma-separated hostnames or IP addresses accepted by Django. | `localhost, 127.0.0.1, 0.0.0.0` |
| `DEBUG` | Enables debug mode only when set to the exact lowercase value `true`. | `true` |
| `AUTHOR` | Optional name displayed in the website footer. | Not set |

Restart the server after changing the configuration. SQLite data is stored in `src/db.sqlite3`; uploaded and seeded images are stored in `src/media/`.

### Sample data

From `src`, populate the database after applying migrations:

```shell
python manage.py seed_db
```

The command creates sample categories and products and copies bundled product images into the media directory. Running it again skips entries with existing names and restores missing seed images; it does not overwrite existing product details.

## Development

With the virtual environment activated, run the code checks from the repository root:

```shell
black --check src
isort --check-only src
flake8 src
```

Run the test suite from `src`:

```shell
python manage.py test
```

The tests cover product and category validation, reviews and tag behavior, including duplicate tag names and the placeholder for products without tags. See the [testing guide](docs/testing.md) for coverage commands.

## Running with Docker

Build the image from the repository root:

```shell
docker build -t baby-tools-world:local .
```

Start the container using the configuration created during Quickstart:

```shell
docker run --rm -it --name baby-tools-world -p 8000:8000 --env-file src/.env baby-tools-world:local
```

The entrypoint collects static files, prepares the database and starts the development server. In a second terminal, add sample data and create the container's admin account:

```shell
docker exec baby-tools-world python manage.py seed_db
docker exec -it baby-tools-world python manage.py createsuperuser
```

Open <http://localhost:8000/> or sign in at <http://localhost:8000/admin/>. The database and media remain inside this example container and are discarded when it is removed.

For a separate WSGI server setup with Gunicorn or Waitress, follow the [WSGI guide](docs/wsgi.md).

## Documentation

- [Testing guide](docs/testing.md): Running tests and collecting coverage.
- [WSGI guide](docs/wsgi.md): Running the application with Gunicorn or Waitress.
- [Original Baby Tools World checklist](docs/Baby-Tools-World-Checkliste.md): The supplied course checklist with verified items checked.
- [Submission verification notes](docs/submission-checklist.md): Evidence and outstanding confirmations for the submission checklist.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
