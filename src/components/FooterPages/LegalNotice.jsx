import React from "react";
import { H2, Text } from "../Common/CommonStyles"
import { ContentWrapper } from "../Layout/LayoutStyles";
import strings from "../../localization/strings";

const LegalNotice = () => {
  document.title = strings.legalNoticeLink;

  return (
    <ContentWrapper>
      <H2>Legal Notice</H2>
      <Text>
        GIIKU GAMES GmbH is a company incorporated under German law.<br />
        Mailing Address<br />
        GIIKU GAMES GmbH<br />
        Rehleitenweg 32b<br />
        83026 Rosenheim<br />
        Germany
      </Text>

      <H2>Corporate information</H2>
      <Text>
        Managing Director: Achim Kaspers<br />
        Court of registry: district court of Traunstein<br />
        Trade register number: HRB 27763<br />
        VAT-ID.: DE323063583<br />
        <br />
        Phone: +49 (0) 89 / 210 205 715<br />
        Fax: +49 (0) 89 / 210 205 799<br />
        <br />
        E-Mail:<br />
        info (at) giikugames.com<br />
        press (at) giikugames.com <br />
      </Text>

      <H2>Disclaimer</H2>
      <Text>
        Although every effort is made to present current and accurate information, we cannot assume responsibility for information from external links. The author of each web page is solely responsible for the content of that page. 
      </Text>

      <H2>Content</H2>
      <Text>
        The author reserves the right not to be responsible for the topicality, correctness, completeness or quality of the information provided.<br />
        Liability claims regarding damage caused by the use of any information provided, including any kind of information which is incomplete or incorrect, will therefore be rejected.
      </Text>

      <H2>Referrals and links</H2>
      <Text>
        The author is not responsible for any contents linked or referred to from his pages unless he has full knowledge of illegal contents and would be able to prevent the visitors of his site from viewing those pages.<br />
        If any damage occurs by the use of information presented there, only the author of the respective pages might be liable, not the one who has linked to these pages.<br />
        Furthermore the author is not liable for any postings or messages published by users of discussion boards, guestbooks or mailinglists provided on his page.<br />
      </Text>

      <H2>Copyright</H2>
      <Text>
        The author intended not to use any copyrighted material for the publication or, if not possible, to indicate the copyright of the respective object.<br />
        The copyright for any material created by the author is reserved. Any duplication or use of objects such as diagrams, sounds or texts in other electronic or printed publications is not permitted without the author's agreement.<br /> 
      </Text>

      <H2>Legal Validity of this Disclaimer</H2>
      <Text>
        This disclaimer is to be regarded as part of the internet publication which you were referred from. If sections or individual terms of this statement are not legal or correct, the content or validity of the other parts remain uninfluenced by this fact. 
      </Text>

      <Text>
        © 2019 GIIKU GAMES GmbH (limited liability)<br/>
        All rights reserved.
      </Text>
    </ContentWrapper>
  )
}

export default LegalNotice;