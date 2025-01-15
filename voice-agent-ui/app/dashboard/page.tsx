"use client";

import Image from "next/image";
import GitHubButton from "react-github-btn";
import Link from "next/link";

export const runtime = "edge";
import { init } from "@fullstory/browser";
import { useEffect } from "react";
import ConversationAgent from "../components/ConversationAgent";

export default function Home() {
  useEffect(() => {
    init({ orgId: "5HWAN" });
  }, []);

  return (
    <>
      <div className="h-full flex overflow-hidden">
        
        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          {/* Top Bar */}
          <div className="bg-gradient-to-b from-black/50 to-black/10 backdrop-blur-[2px] h-[4rem] flex items-center">
            <header className="mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8 flex items-center justify-end pt-4 md:pt-0 gap-2">
              <div className="flex items-center justify-center md:gap-6 text-sm">
                <span className="mt-1">
                  <GitHubButton
                    href="https://github.com/himanshu-skid19/encode-2025/"
                    data-color-scheme="no-preference: light; light: light; dark: light;"
                    data-size="large"
                    data-show-count="true"
                    aria-label="Star deepgram-devs/deepgram-conversational-demo on GitHub"
                  >
                    Star
                  </GitHubButton>
                </span>

                <span className="gradient-shadow bg-gradient-to-r to-[#13EF93]/50 from-[#149AFB]/80 rounded">
                  <a
                    href="https://console.deepgram.com/signup?jump=keys"
                    target="_blank"
                    className="hidden text-xs md:inline-block bg-black text-white rounded m-px px-8 py-2 font-semibold"
                  >
                    Get an API Key
                  </a>
                </span>
              </div>
            </header>
          </div>

          {/* Main Section */}
          <main className="mx-auto max-w-7xl px-4 md:px-6 lg:px-8 h-[calc(100%-10rem)]">
            <ConversationAgent />
          </main>

          {/* Footer */}
          <div className="backdrop-blur-[2px] h-[4rem] flex items-center">
            <footer className="mx-auto w-full max-w-7xl px-4 md:px-6 lg:px-8 flex items-center justify-center">
              <Link
                href="https://forms.office.com/r/hGJDf68aSA"
                className="bg-gradient-to-r from-[#149AFB] to-[#13EF93] text-white px-8 py-2 rounded-md hover:opacity-90 transition-opacity font-medium flex items-center gap-2"
                target="_blank"
              >
                Contact Us for Phone Support
              </Link>
            </footer>
          </div>
        </div>
      </div>
    </>
  );
}
