# Compile an app on a web farm | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 294
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/creatio-maintenance/compile_app_on_web_farm

## Description

If you use a load balancer to ensure fault tolerance of your Creatio
application, the processes that involve the app compilation differ. You must
perform the setup on one Creatio instance, then transfer the settings to other
instances.

## Key Concepts

configuration, database, package, marketplace

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)**
(8.3).

Version: 8.0

On this page

If you use a load balancer to ensure fault tolerance of your Creatio
application, the processes that involve the app compilation differ. You must
perform the setup on one Creatio instance, then transfer the settings to other
instances.

Creatio runs the compilation automatically when you execute the following
actions:

- set up record permissions
- set up the changelog
- activate an additional UI language
- install packages that contain changes created and tested on other environments
  into a production environment
- install a Marketplace application.

note

We recommend performing the setup outside business hours since Creatio will be
unavailable.

View the general procedure to follow when Creatio compiles the app automatically
below. The specifics might vary based on the load balancer you use with your
Creatio application.

### General setup procedure​

1. **Set up a redirect** to the placeholder page that explains the reasons for
   the downtime in the load balancer. Learn more about setting up redirects in
   the vendor documentation. For example,
   [HAProxy Enterprise](https://www.haproxy.com/documentation/hapee/latest/traffic-routing/redirects/).

2. **Stop all Creatio instances** except one. Learn more in the Update guide:
   [Stopping the site](https://academy.creatio.com/node/143#title-143-13).

3. **Back up** the database. Learn more in the Update guide:
   [Creating database backup](https://academy.creatio.com/node/143#title-143-2).

4. Perform the required process.

5. **Apply the changes** on the web farm level. To do this, copy the contents of
   the following folders to every Creatio instance:
   - WebApp/conf/ and WebApp/Terrasoft.Configuration/Pkg for Creatio **NET
     Framework**
   - Creatio root folder for Creatio **.NET Core**

6. **Flush** Redis.

7. **Start** the stopped Creatio instances. Learn more in the Update guide:
   [Website starting, compilation and verification](https://academy.creatio.com/node/143#title-143-14).

8. **Disable the redirect** in the load balancer.

---

## See also​

[System requirements calculator](https://academy.creatio.com/docs/calculator)

[HAProxy Enterprise](https://www.haproxy.com/documentation/hapee/latest/traffic-routing/redirects/)

[Update guide](https://academy.creatio.com/setup-and-administration/category/on-site-deployment)

- General setup procedure
- See also
