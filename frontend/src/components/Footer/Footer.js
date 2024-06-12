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
            <NavLink href="https://vi.wikipedia.org/wiki/%C4%90%C3%A0_L%E1%BA%A1t">
              Đà Lạt
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="https://hcmute.edu.vn/" target="_blank">
              HCMUTE
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="https://feee.hcmute.edu.vn/" target="_blank"> 
              Khoa Điện - Điện Tử
            </NavLink>
          </NavItem>
        </Nav>
        <div className="copyright">
          © {new Date().getFullYear()} {" "}
          <i className="tim-icons icon-heart-2" /> {" "}
          <a
            href="https://feee.hcmute.edu.vn/"
            target="_blank"
          >
            Khoa Điện - Điện Tử
          </a>{" "}
          HCMUTE
        </div>
      </Container>
    </footer>
  );
}

export default Footer;
