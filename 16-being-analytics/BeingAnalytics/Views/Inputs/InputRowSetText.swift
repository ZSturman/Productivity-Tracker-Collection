//
//  InputRowSetText.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
// 

import SwiftUI

struct InputRowSetText: View {
    
    @Binding var setValue: String
    
    var body: some View {
        VStack {
            HStack {
                Image(systemName: "textformat")
                    .foregroundColor(.gray)
                    .font(.headline)
                TextField("Enter text value...", text: $setValue)
            }
            .padding()
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.gray, lineWidth: 1))
            
        }
    }
}
