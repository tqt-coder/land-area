/*!

=========================================================
=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container, Nav, NavItem, NavLink } from "reactstrap";

function Footer() {
  return (
    <footer className="footer">
      <Container fluid>
        <Nav>
          <NavItem>
            <NavLink href="https://www.creative-tim.com/?ref=bdr-user-archive-footer">
              Land Area Statistics
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="https://www.facebook.com/vinhcet.11011917" target="_blank">
              About Us
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="https://www.facebook.com/vinhcet.11011917" target="_blank"> 
              Blog
            </NavLink>
          </NavItem>
        </Nav>
        <div className="copyright">
          © {new Date().getFullYear()} made with{" "}
          <i className="tim-icons icon-heart-2" /> by{" "}
          <a
            href="https://www.creative-tim.com/?ref=bdr-user-archive-footer"
            target="_blank"
          >
            UTE
          </a>{" "}
          Land Area Statistics
        </div>
      </Container>
    </footer>
  );
}

export default Footer;
