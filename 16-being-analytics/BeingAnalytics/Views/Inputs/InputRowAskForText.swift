//
//  InputRowAskForText.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
//

import SwiftUI

struct InputRowAskForText: View {
    
    @Binding var promptBool: Bool
    @Binding var allowBlank: Bool
    @Binding var defaultBool: Bool
    @Binding var promptString: String
    @Binding var defaultString: String

    var body: some View {
        VStack {
            HStack {
                Image(systemName: "ellipsis.message")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $promptBool, label: {
                    Text("Display prompt?")
                })
            }

            if promptBool {
                HStack {
                    Image(systemName: "textformat")
                        .foregroundColor(.gray)
                        .font(.headline)
                    TextField("Enter prompt text", text: $promptString)
                }
                .padding()
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            }

            HStack {
                Image(systemName: "circle.slash")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $allowBlank, label: {
                    Text("Allow blank?")
                })
            }

            HStack {
                Image(systemName: "line.2.horizontal.decrease.circle")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $defaultBool, label: {
                    Text("Set default value?")
                })
            }

            if defaultBool {
                HStack {
                    Image(systemName: "text.cursor")
                        .foregroundColor(.gray)
                        .font(.headline)
                    TextField("Enter default value", text: $defaultString)
                }
                .padding()
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            }
       }
    }
}


