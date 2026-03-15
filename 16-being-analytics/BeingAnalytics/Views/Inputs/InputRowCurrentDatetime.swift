//
//  InputRowCurrentDatetime.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/12/23.
//

import SwiftUI 

struct InputRowCurrentDatetime: View {
    
    @Binding var collectDate: Bool
    @Binding var collectTime: Bool
    
    var body: some View {
        VStack {
            HStack {
                Image(systemName: "calendar")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $collectDate, label: {
                    Text("Collect date?")
                })
            }
            
            HStack {
                Image(systemName: "clock.fill")
                    .foregroundColor(.gray)
                    .font(.headline)
                Toggle(isOn: $collectTime, label: {
                    Text("Collect time?")
                })
            }
       }
    }
}
