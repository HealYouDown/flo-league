import React from "react";
import { H2, Text } from "../Common/CommonStyles"
import { ContentWrapper } from "../Layout/LayoutStyles";
import strings from "../../localization/strings";

const PrivacyPolicy = () => {
  document.title = strings.privacyPolicyLink;

  return (
    <ContentWrapper>
      <H2>{strings.privacyPolicyHeader}</H2>
      <Text>{strings.privacyPolicyText}</Text>
    </ContentWrapper>
  )
}

export default PrivacyPolicy;